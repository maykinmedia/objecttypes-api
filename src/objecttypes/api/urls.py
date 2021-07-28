from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path("v1", include("objecttypes.api.v1.urls", namespace="v1")),
    path("v2", include("objecttypes.api.v2.urls", namespace="v2")),
]
