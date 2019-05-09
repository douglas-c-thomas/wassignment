from django.conf.urls import url, include

urlpatterns = [
    url(r'bls-dataset/', include('bls_dataset.urls')),
]
