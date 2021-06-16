from django.utils.translation import ugettext_lazy as _

from drf_spectacular.openapi import AutoSchema as _AutoSchema
from drf_spectacular.utils import OpenApiParameter

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
        return content_type_headers

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
