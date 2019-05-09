from bls_dataset.views import QueryListCreateView, QueryRetrieveView
from django.conf.urls import url

urlpatterns = [
    # Queries
    url(r'^queries$', QueryListCreateView.as_view()),
    url(r'^queries/(?P<uuid>[\w\-]+)/$', QueryRetrieveView.as_view()),
]

