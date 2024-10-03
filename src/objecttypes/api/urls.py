from django.urls import include, path

urlpatterns = [
    path("v2", include("objecttypes.api.v2.urls", namespace="v2")),
]
