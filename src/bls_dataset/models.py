from django.db import models
import uuid


class Query(models.Model):
    """
    The Query represents the meta data of collection of data records gathered in a single request query.
    """
    # The UUID
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4)

    # The name to apply to the query result set
    name = models.CharField(null=True, blank=True, max_length=32)

    # The original request data sent by the user
    query_parameters = models.TextField(null=True, blank=True)

    # Date the query was executed
    date_time = models.DateTimeField(auto_now=False, auto_now_add=True)

    # The raw result set returned by the Big Query API
    query_results = models.TextField(null=True, blank=True)

    def to_json(self):
        """
        Convert the Query model to a JSON representation

        :return: The JSON representation
        """
        return {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'query_parameters': self.query_parameters,
            'date_time': self.date_time.isoformat(),
            'query_results': self.query_results
        }
