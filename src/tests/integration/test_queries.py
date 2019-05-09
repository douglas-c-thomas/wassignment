import json
import logging
import random

import http.client
import nose.tools
import requests
from django.test import TestCase

logger = logging.getLogger('__name__')


class TestQueries(TestCase):
    """
    Integration tests for the Query APIs
    """
    def setUp(self):
        """
        Set up
        """
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer MAGIC_KEY'
        }

    def test_successful_post(self):
        """
        Test a successful query post
        """
        query_data = {
            'dataset': 'unemployment_cps',
            'name': 'CPS Test',
            'query': {
                'year': 1956
            },
            'limit': 1
        }
        response = requests.post('http://0.0.0.0:8000/bls-dataset/queries', headers=self.headers,
                                 data=json.dumps(query_data))
        response_data = response.json()

        # Test out the API response
        nose.tools.assert_equals(response.status_code, http.client.CREATED)
        nose.tools.assert_is_not_none(response_data.get('id'))
        nose.tools.assert_is_not_none(response_data.get('uuid'))
        nose.tools.assert_is_not_none(response_data.get('name'))
        nose.tools.assert_equals(response_data.get('name'), 'CPS Test')
        nose.tools.assert_is_not_none(response_data.get('date_time'))

        nose.tools.assert_is_not_none(response_data.get('query_parameters'))
        query_parameters = json.loads(response_data.get('query_parameters'))
        nose.tools.assert_equals(query_parameters.get('dataset'), 'unemployment_cps')

        nose.tools.assert_is_not_none(response_data.get('query_results'))
        query_results = json.loads(response_data.get('query_results'))
        nose.tools.assert_equals(query_results.get('data')[0].get('year'), 1956)

    def test_successful_query_by_index(self):
        """
        Test a successful index query
        """
        response = requests.get('http://0.0.0.0:8000/bls-dataset/queries', headers=self.headers)
        response_data = response.json()

        # Test out the API response
        nose.tools.assert_equals(response.status_code, http.client.OK)
        nose.tools.assert_is_not_none(response_data)
        nose.tools.assert_is_instance(response_data, list)
        nose.tools.assert_is_not_none(len(response_data), 0)

        # Test out a sample query result
        query_result = response_data[0]
        nose.tools.assert_is_not_none(query_result.get('id'))
        nose.tools.assert_is_not_none(query_result.get('uuid'))
        nose.tools.assert_is_not_none(query_result.get('name'))
        nose.tools.assert_is_not_none(query_result.get('date_time'))
        nose.tools.assert_is_not_none(query_result.get('query_parameters'))
        nose.tools.assert_is_not_none(query_result.get('query_results'))

    def test_successful_query_by_uuid(self):
        """
        Test a successful query by uuid
        """
        query_data = {
            'dataset': 'unemployment_cps',
            'name': 'CPS Test',
            'query': {
                'year': 1948
            },
            'limit': 1
        }
        post_response = requests.post('http://0.0.0.0:8000/bls-dataset/queries', headers=self.headers,
                                      data=json.dumps(query_data))
        post_response_data = post_response.json()
        uuid = post_response_data.get('uuid')

        get_response = requests.get('http://0.0.0.0:8000/bls-dataset/queries/{}'.format(uuid), headers=self.headers)
        get_response_data = get_response.json()

        # Test out the API responses
        nose.tools.assert_equals(post_response.status_code, http.client.CREATED)
        nose.tools.assert_equals(get_response.status_code, http.client.OK)

        nose.tools.assert_is_not_none(get_response_data.get('id'))
        nose.tools.assert_is_not_none(get_response_data.get('uuid'))
        nose.tools.assert_equals(get_response_data.get('uuid'), uuid)
        nose.tools.assert_is_not_none(get_response_data.get('name'))
        nose.tools.assert_is_not_none(get_response_data.get('date_time'))
        nose.tools.assert_is_not_none(get_response_data.get('query_parameters'))
        nose.tools.assert_is_not_none(get_response_data.get('query_results'))

    def test_successful_query_by_name(self):
        """
        Test a successful query by name
        """
        test_name = 'CPS Test {}'.format(random.randint(1, 10000000000))

        query_data = {
            'dataset': 'unemployment_cps',
            'name': test_name,
            'query': {
                'year': 1984
            },
            'limit': 1
        }
        post_response = requests.post('http://0.0.0.0:8000/bls-dataset/queries', headers=self.headers,
                                      data=json.dumps(query_data))

        get_response = requests.get('http://0.0.0.0:8000/bls-dataset/queries?name={}'.format(test_name),
                                    headers=self.headers)
        get_response_data = get_response.json()

        # Test out the API responses
        nose.tools.assert_equals(post_response.status_code, http.client.CREATED)
        nose.tools.assert_equals(get_response.status_code, http.client.OK)
        nose.tools.assert_is_instance(get_response_data, list)
        nose.tools.assert_equals(len(get_response_data), 1)

        # Test out a the query result
        query_result = get_response_data[0]
        nose.tools.assert_is_not_none(query_result.get('id'))
        nose.tools.assert_is_not_none(query_result.get('uuid'))
        nose.tools.assert_is_not_none(query_result.get('name'))
        nose.tools.assert_equals(query_result.get('name'), test_name)
        nose.tools.assert_is_not_none(query_result.get('date_time'))
        nose.tools.assert_is_not_none(query_result.get('query_parameters'))
        nose.tools.assert_is_not_none(query_result.get('query_results'))

    def test_invalid_limit(self):
        """
        Test a query with an invalid limit
        """
        query_data = {
            'dataset': 'unemployment_cps',
            'name': 'CPS Test',
            'query': {
                'year': 1973
            },
            'limit': 666
        }
        response = requests.post('http://0.0.0.0:8000/bls-dataset/queries', headers=self.headers,
                                 data=json.dumps(query_data))

        # Test out the API response
        nose.tools.assert_equals(response.status_code, http.client.BAD_REQUEST)
        nose.tools.assert_equals(response.json().pop(), 'The limit cannot be exactly 666.')

    def test_improper_authorization(self):
        """
        Test a query with an improper authorization token
        """
        bad_header = self.headers.copy()
        bad_header['Authorization'] = 'Bearer BLACK_MAGIC_KEY'

        query_data = {
            'dataset': 'unemployment_cps',
            'name': 'CPS Test',
            'query': {
                'year': 1973
            },
            'limit': 666
        }
        response = requests.post('http://0.0.0.0:8000/bls-dataset/queries', headers=bad_header,
                                 data=json.dumps(query_data))

        # Test out the API response
        nose.tools.assert_equals(response.status_code, http.client.FORBIDDEN)
        nose.tools.assert_equals(response.json(), {'detail': 'Authentication credentials were not provided.'})
