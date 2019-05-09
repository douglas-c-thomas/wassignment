from bls_dataset.models import Query
from bls_dataset.serializers import QuerySerializer
from django.db.models import Q
from rest_framework import generics

from bls_dataset.permissions import HasAPIKeyPermission


class QueryListCreateView(generics.ListCreateAPIView):
    """
    The QueryListCreateView DRF view handles the URL pattern for /queries.  For POST requests, new queries are executed
    against the BLS Big Query dataset based upon query parameters in the request payload and the result set is
    persisted.  For GET requests, a list of the data surrounding the executed queries are returned.
    """
    serializer_class = QuerySerializer
    permission_classes = (HasAPIKeyPermission,)

    def perform_create(self, serializer):
        """
        Create a Query instance

        :param serializer: The QuerySerializer
        """
        serializer.validated_data['request_data'] = self.request.data
        super(generics.ListCreateAPIView, self).perform_create(serializer)

    def get_queryset(self):
        """
        Queries could be filtered by name

        :return: The matching list of query instances
        """
        query = []

        if self.request.query_params.get('name'):
            query.append(Q(name=self.request.query_params.get('name')))

        return Query.objects.filter(*query)


class QueryRetrieveView(generics.RetrieveAPIView):
    """
    The QueryRetrieveView DRF view handles the URL pattern for /queries/<uuid>.
    """
    serializer_class = QuerySerializer
    permission_classes = (HasAPIKeyPermission,)
    queryset = Query.objects.all()
    lookup_field = 'uuid'

