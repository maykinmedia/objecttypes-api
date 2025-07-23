from django.utils.translation import gettext_lazy as _

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

from objecttypes.core.constants import ObjectVersionStatus
from objecttypes.core.models import ObjectType, ObjectVersion
from objecttypes.token.models import TokenAuth

from ..filters import ObjectTypeFilterSet
from ..mixins import NestedViewSetMixin
from ..pagination import DynamicPageSizePagination
from ..serializers import ObjectTypeSerializer, ObjectVersionSerializer

logger = structlog.stdlib.get_logger(__name__)


@extend_schema_view(
    retrieve=extend_schema(operation_id="objecttype_read"),
    destroy=extend_schema(operation_id="objecttype_delete"),
)
class ObjectTypeViewSet(viewsets.ModelViewSet):
    queryset = ObjectType.objects.prefetch_related("versions").order_by("-pk")
    serializer_class = ObjectTypeSerializer
    lookup_field = "uuid"
    filterset_class = ObjectTypeFilterSet
    pagination_class = DynamicPageSizePagination

    def perform_create(self, serializer):
        super().perform_create(serializer)
        obj = serializer.instance
        token_auth: TokenAuth = self.request.auth
        logger.info(
            "objecttype_created",
            uuid=str(obj.uuid),
            name=obj.name,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    def perform_update(self, serializer):
        super().perform_update(serializer)
        obj = serializer.instance
        token_auth: TokenAuth = self.request.auth
        logger.info(
            "objecttype_updated",
            uuid=str(obj.uuid),
            name=obj.name,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    def perform_destroy(self, instance):
        if instance.versions.exists():
            raise ValidationError(
                {
                    api_settings.NON_FIELD_ERRORS_KEY: [
                        _(
                            "All related versions should be destroyed before destroying the objecttype"
                        )
                    ]
                },
                code="pending-versions",
            )

        super().perform_destroy(instance)
        token_auth: TokenAuth = self.request.auth
        logger.info(
            "objecttype_deleted",
            uuid=str(instance.uuid),
            name=instance.name,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )


@extend_schema_view(
    retrieve=extend_schema(
        operation_id="objectversion_read",
        description=_("Retrieve an OBJECTTYPE with the given version."),
    ),
    list=extend_schema(
        operation_id="objectversion_list",
        description=_("Retrieve all versions of an OBJECTTYPE"),
    ),
    create=extend_schema(
        operation_id="objectversion_create",
        description=_("Create an OBJECTTYPE with the given version."),
    ),
    destroy=extend_schema(
        operation_id="objectversion_delete",
        description=_("Destroy the given OBJECTTYPE."),
    ),
    update=extend_schema(
        operation_id="objectversion_update",
        description=_("Update an OBJECTTYPE with the given version."),
    ),
    partial_update=extend_schema(
        operation_id="objectversion_partial_update",
        description=_("Partially update an OBJECTTYPE with the given version."),
    ),
)
class ObjectVersionViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = ObjectVersion.objects.order_by("object_type", "-version")
    serializer_class = ObjectVersionSerializer
    lookup_field = "version"
    pagination_class = DynamicPageSizePagination

    def perform_create(self, serializer):
        super().perform_create(serializer)
        obj = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "object_version_created",
            version=str(obj.version),
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    def perform_update(self, serializer):
        super().perform_update(serializer)
        obj = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "object_version_updated",
            version=str(obj.version),
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    def perform_destroy(self, instance):
        if instance.status != ObjectVersionStatus.draft:
            raise ValidationError(
                {
                    api_settings.NON_FIELD_ERRORS_KEY: [
                        _("Only draft versions can be destroyed")
                    ]
                },
                code="non-draft-version-destroy",
            )

        super().perform_destroy(instance)
        token_auth = self.request.auth
        logger.info(
            "object_version_deleted",
            version=str(instance.version),
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )
