from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView

import structlog
from drf_spectacular.views import (
    SpectacularJSONAPIView as _SpectacularJSONAPIView,
    SpectacularYAMLAPIView as _SpectacularYAMLAPIView,
)
from open_api_framework.conf.utils import config
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = structlog.stdlib.get_logger(__name__)

DEFAULT_CODE = "invalid"
DEFAULT_DETAIL = _("Invalid input.")


def exception_handler(exc, context):
    """
    Transform 5xx errors into DSO-compliant shape.
    """
    response = drf_exception_handler(exc, context)
    if not response:
        if config("DEBUG", default=False):
            return None

        data = {
            "code": "error",
            "title": "Internal Server Error",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": _("A server error has occurred."),
        }
        event = "api.uncaught_exception"

        response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=data)
        logger.exception(event, exc_info=exc)

        return response

    # exception logger event
    logger.exception(
        "api.handled_exception",
        title=getattr(exc, "default_detail", DEFAULT_DETAIL).strip("'"),
        code=getattr(exc, "default_code", DEFAULT_CODE),
        status=getattr(response, "status_code", status.HTTP_400_BAD_REQUEST),
        data=getattr(response, "data", {}),
        exc_info=False,
    )

    return response


class AllowAllOriginsMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = "*"
        return response


class SpectacularYAMLAPIView(AllowAllOriginsMixin, _SpectacularYAMLAPIView):
    """Spectacular YAML API view with Access-Control-Allow-Origin set to allow all"""


class SpectacularJSONAPIView(AllowAllOriginsMixin, _SpectacularJSONAPIView):
    """Spectacular JSON API view with Access-Control-Allow-Origin set to allow all"""


class DeprecationRedirectView(RedirectView):
    def get(self, request, *args, **kwargs):
        logger.warning(
            "deprecated_endpoint_called",
            endpoint=request.path,
        )
        return super().get(request, *args, **kwargs)
