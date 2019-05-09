import json
import uuid
import factory.fuzzy
import faker
from bls_dataset.models import Query
from datetime import datetime

faker = faker.Factory.create()

"""
Factory Boy documentation:  https://factoryboy.readthedocs.io/en/latest/
"""


class QueryFactory(factory.DjangoModelFactory):
    """
    Factory for creating a Query instance
    """
    class Meta:
        model = Query

    # The UUID
    uuid = uuid.uuid4()

    # The name to apply to the query result set
    name = factory.Sequence(lambda n: 'CPS Test Query {}'.format(n))

    # The original request data sent by the user
    query_parameters = json.dumps({
        "dataset": "unemployment_cps",
        "name": "CPS-1950",
        "query": {"year": 1950},
        "limit": 5
    })

    # Date the query was executed
    date_time = datetime.utcnow()

    # The raw result set returned by the Big Query API
    query_results = json.dumps({
        "size": 1,
        "data": [{
            "series_id": "LNS11000025",
            "year": 1950,
            "period": "M01",
            "value": 41129.0,
            "footnote_codes": None,
            "date": "1950-01-01",
            "series_title": "(Seas) Civilian Labor Force Level - 20 yrs. & over, Men"
        }]
    })
