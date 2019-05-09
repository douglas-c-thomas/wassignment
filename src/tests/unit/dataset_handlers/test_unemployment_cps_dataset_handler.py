import json

import nose.tools
from dataset_handlers.unemployment_cps_dataset_handler import UnemploymentCPSDatasetHandler
from django.test import TestCase


class TestUnemploymentCPSDatasetHandler(TestCase):
    """
    Unit tests for handling the retrieval of Big Query datasets
    """

    def setUp(self):
        """
        Set up some fixtures
        """
        self.dataset_handler = UnemploymentCPSDatasetHandler()
        self.dataset = 'unemployment_cps'

    def test_execute_query(self):
        """
        Test out various queries exercising the dataset handler's execute_query function.
        """
        # Test a query by year with limit 1
        results = json.loads(self.dataset_handler.execute_query(self.dataset, {'year': 1948}, 1))
        nose.tools.assert_equals(results.get('size'), 1)
        data_set = results.get('data')
        nose.tools.assert_is_not_none(data_set)
        data = data_set.pop()
        nose.tools.assert_equals(data.get('year'), 1948)

        # Test a query by series_id with limit 100
        results = json.loads(self.dataset_handler.execute_query(self.dataset, {'series_id': 'LNS12000164'}, 100))
        nose.tools.assert_equals(results.get('size'), 100)
        data_set = results.get('data')
        nose.tools.assert_is_not_none(data_set)
        data = data_set.pop()
        nose.tools.assert_equals(data.get('series_id'), 'LNS12000164')

        #
        # Could do other tests like these, but these cover the very basics ...
        #
