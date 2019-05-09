import importlib
import json
import logging

from bls_dataset.models import Query
from dataset_handlers.dataset_handler import DatasetHandler
from rest_framework import serializers

logger = logging.getLogger('__name__')


class QuerySerializer(serializers.ModelSerializer):
    """
    The QuerySerializer serializes the query data to the python models
    """
    class Meta:
        model = Query
        fields = ('id', 'uuid', 'name', 'query_parameters', 'date_time', 'query_results')

    def create(self, validated_data):
        """
        Create and return a new Query instance given the validated data.  Additionally, execute the query by sending
        the query parameters to the BLS data set in the Google Big Query data repositories.

        :param validated_data: The validated request data
        :return: The create Query instance with the appropriate values
        """
        # Pull the request_data off the validated data and set up for query execution
        request_data = validated_data.pop('request_data')
        dataset = request_data.get('dataset')
        query_parameters = request_data.get('query')
        validated_data['query_parameters'] = json.dumps(request_data)

        # Validate that the limit isn't 666
        limit = request_data.get('limit', 100)
        if limit == 666:
            raise serializers.ValidationError('The limit cannot be exactly 666.')

        # Instantiate a dataset handler.  Use a factory type method to create the appropriate dataset handler.
        module = importlib.import_module('dataset_handlers.{}_dataset_handler'.format(dataset))
        dataset_handler_class = getattr(module, DatasetHandler.get_class_for_dataset(dataset))
        dataset_handler = dataset_handler_class()

        # Delegate query execution to the data handler
        results = dataset_handler.execute_query(dataset, query_parameters, limit)

        # Persist the Query model
        query = Query(**validated_data)
        query.query_results = results
        query.save()

        logger.info('Persisted a query: {}'.format(query.to_json()))
        return query
