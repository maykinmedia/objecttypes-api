from django.conf.urls import include
from django.urls import path

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


urlpatterns = [
    path("v1/", include(router.urls)),
    path(
        "v1/",
        include(
            [
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
            ]
        ),
    ),
    path(
        "v1",
        SpectacularJSONAPIView.as_view(),
        name="schema-json",
    ),
]
