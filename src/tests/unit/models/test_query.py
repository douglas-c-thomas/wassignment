import nose.tools
from django.test import TestCase
from datetime import datetime

from tests.model_factories import QueryFactory


class TestQuery(TestCase):
    """
    Model tests for the Query model object.  Use Factory Boy to set up the test data in the model_factories.py.
    """

    def setUp(self):
        """
        Set up some queries to test out
        """
        self.queries = [QueryFactory.create() for q in range(5)]

    def tearDown(self):
        """
        Remove all of the test queries
        """
        for query in self.queries:
            query.delete()

    def test_to_json(self):
        """
        Test out the to_json function
        """
        for query in self.queries:
            query_json = query.to_json()
            nose.tools.assert_is_not_none(query_json.get('uuid'))
            nose.tools.assert_in('CPS Test Query', query_json.get('name'))
            nose.tools.assert_is_not_none('query_parameters')
            nose.tools.assert_is_not_none(query_json.get('date_time'))
            nose.tools.assert_is_not_none('query_results')
