from django.urls import include, path

from drf_spectacular.views import SpectacularRedocView
from vng_api_common import routers

from objecttypes.utils.views import (
    DeprecationRedirectView,
    SpectacularJSONAPIView,
    SpectacularYAMLAPIView,
)

from .views import ObjectTypeViewSet, ObjectVersionViewSet

router = routers.DefaultRouter()
router.register(
    r"objecttypes",
    ObjectTypeViewSet,
    [routers.Nested("versions", ObjectVersionViewSet)],
)


app_name = "v2"

urlpatterns = [
    path(
        "/",
        include(
            [
                # schema
                path(
                    "schema/openapi.yaml",
                    DeprecationRedirectView.as_view(pattern_name="v2:schema"),
                ),
                path(
                    "openapi.yaml",
                    SpectacularYAMLAPIView.as_view(),
                    name="schema",
                ),
                path(
                    "openapi.json",
                    SpectacularJSONAPIView.as_view(),
                    name="schema-json",
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
