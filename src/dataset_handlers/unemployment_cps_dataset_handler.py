import json
import logging

from dataset_handlers.dataset_handler import DatasetHandler

logger = logging.getLogger('__name__')


class UnemploymentCPSDatasetHandler(DatasetHandler):
    """
    The UnemploymentCPSDatasetHandler knows how to execute queries against the bls.unemployment_cps dataset an can
    properly persist UnemploymentDataQueryResult model instances.
    """
    def __init__(self):
        """
        The execute_query function implements the query execution against a particular BLS dataset

        :param dataset: The dataset in question
        :param query:  The query parameters to send to the Google Big Query engine
        :param limit: The maximum number of records to return
        :return: A Big Query Result Set
        """
        super(UnemploymentCPSDatasetHandler, self).__init__()

    def execute_query(self, dataset, query, limit):
        """
        The execute_query function implements the query execution against the bls.unemployment_cps.

        The assignment asks to handle query input by year.  I show how `series_id` and `period` can be handled to show
        multiple query parameters as well, but ditch the others since it is really out of scope.  We can add it as
        technical debt to handle the other query columns later.

        :param dataset: The dataset in question
        :param query:  The query parameters to send to the Google Big Query engine
        :param limit: The maximum number of records to return
        :return: A Big Query Result Set
        """
        results = {}
        filter_clause = ''
        if 'year' in query.keys():
            filter_clause += 'year={} AND'.format(query.get('year'))
        if 'series_id' in query.keys():
            filter_clause += 'series_id="{}" AND'.format(query.get('series_id'))
        if 'period' in query.keys():
            filter_clause += 'period="{}" AND'.format(query.get('period'))

        # Trim the trailing ' AND'
        filter_clause = filter_clause[:-4]

        # Create the Big Query query
        client_query = """
            SELECT * 
            FROM `{dataset_name}` 
            WHERE {filter_clause} 
            LIMIT {limit}
        """.format(dataset_name='bigquery-public-data.bls.{}'.format(dataset), filter_clause=filter_clause, limit=limit)

        try:
            # Execute the query in the Big Query engine
            query_job = self.client.query(client_query)
            query_results = query_job.result()
        except Exception as e:
            logger.exception('Exception caught during querying the Big Query datasets:\n{}'.format(str(e)))
            raise e

        # Process the results
        results_data = []
        size = 0
        for result in query_results:
            results_data.append({
                'series_id': result.get('series_id'),
                'year': result.get('year'),
                'period': result.get('period'),
                'value': result.get('value'),
                'footnote_codes': result.get('footnote_codes'),
                'date': result.get('date').strftime('%Y-%m-%d'),
                'series_title': result.get('series_title')
            })
            size += 1

        results['size'] = size
        results['data'] = results_data
        return json.dumps(results)
