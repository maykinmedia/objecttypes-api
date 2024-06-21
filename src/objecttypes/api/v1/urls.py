from django.urls import include, path

from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularYAMLAPIView,
)
from vng_api_common import routers

from .views import ObjectTypeViewSet, ObjectVersionViewSet

router = routers.DefaultRouter()
router.register(
    r"objecttypes",
    ObjectTypeViewSet,
    [routers.nested("versions", ObjectVersionViewSet)],
)


app_name = "v1"

urlpatterns = [
    path("", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path(
        "/",
        include(
            [
                # schema
                path(
                    "schema/openapi.yaml",
                    SpectacularYAMLAPIView.as_view(),
                    name="schema",
                ),
                path(
                    "schema/",
                    SpectacularRedocView.as_view(url_name="schema"),
                    name="schema-redoc",
                ),
                # actual endpoints
                path("", include(router.urls)),
            ]
        ),
    ),
]
