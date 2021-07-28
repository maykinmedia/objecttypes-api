from uuid import UUID

from django.utils.translation import ugettext_lazy as _

from drf_spectacular.openapi import AutoSchema as _AutoSchema
from drf_spectacular.utils import OpenApiParameter
from rest_framework.test import APIRequestFactory
from rest_framework_nested.viewsets import NestedViewSetMixin
from vng_api_common.inspectors.view import HTTP_STATUS_CODE_TITLES


class AutoSchema(_AutoSchema):
    def get_operation_id(self):
        """
        Use model name as a base for operation_id
        """
        if hasattr(self.view, "queryset"):
            model_name = self.view.queryset.model._meta.model_name
            return f"{model_name}_{self.view.action}"
        return super().get_operation_id()

    def get_override_parameters(self):
        content_type_headers = self.get_content_type_headers()
        parent_path_headers = self.get_parent_path_headers()
        return content_type_headers + parent_path_headers

    def _get_response_for_code(self, serializer, status_code, media_types=None):
        """ add default description to the response """
        response = super()._get_response_for_code(serializer, status_code, media_types)

        if not response.get("description"):
            response["description"] = HTTP_STATUS_CODE_TITLES.get(int(status_code))
        return response

    def get_content_type_headers(self) -> list:
        if self.method not in ["POST", "PUT", "PATCH"]:
            return []

        return [
            OpenApiParameter(
                name="Content-Type",
                type=str,
                location=OpenApiParameter.HEADER,
                required=True,
                enum=["application/json"],
                description=_("Content type of the request body."),
            )
        ]

    def get_parent_path_headers(self) -> list:
        """ for nested viewsets """
        if not isinstance(self.view, NestedViewSetMixin):
            return []

        parent_lookup_kwargs = self.view._get_parent_lookup_kwargs()
        path_params = list(parent_lookup_kwargs.keys())

        return [
            OpenApiParameter(
                name=path_param,
                type=UUID if "uuid" in path_param else str,
                location=OpenApiParameter.PATH,
                required=True,
                description=_("Unique identifier (UUID4)")
                if "uuid" in path_param
                else _("Unique identifier"),
            )
            for path_param in path_params
        ]

    def get_tags(self):
        return ["Objecttypes"]


def build_mock_request(method, path, view, original_request, **kwargs):
    """ NestedViewSetMixin requires some tweaking in schema generation """

    request = getattr(APIRequestFactory(), method.lower())(path=path)
    if isinstance(view, NestedViewSetMixin):
        url_kwarg, fk_filter = list(view._get_parent_lookup_kwargs().items())[0]
        kwargs[url_kwarg] = ""
        request = view.initialize_request(request, **kwargs)
    else:
        request = view.initialize_request(request)
    if original_request:
        request.user = original_request.user
        request.auth = original_request.auth
        # ignore headers related to authorization as it has been handled above.
        # also ignore ACCEPT as the MIME type refers to SpectacularAPIView and the
        # version (if available) has already been processed by SpectacularAPIView.
        for name, value in original_request.META.items():
            if not name.startswith("HTTP_"):
                continue
            if name in ["HTTP_ACCEPT", "HTTP_COOKIE", "HTTP_AUTHORIZATION"]:
                continue
            request.META[name] = value
    return request
