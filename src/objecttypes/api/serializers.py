from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from vng_api_common.utils import get_help_text

from objecttypes.core.models import ObjectType, ObjectVersion

from .validators import (
    IsImmutableValidator,
    JsonSchemaValidator,
    VersionUpdateValidator,
)


class ObjectVersionSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {"objecttype_uuid": "object_type__uuid"}

    class Meta:
        model = ObjectVersion
        fields = (
            "url",
            "version",
            "objectType",
            "status",
            "jsonSchema",
            "createdAt",
            "modifiedAt",
            "publishedAt",
        )
        extra_kwargs = {
            "url": {"lookup_field": "version"},
            "version": {"read_only": True},
            "objectType": {
                "source": "object_type",
                "lookup_field": "uuid",
                "read_only": True,
            },
            "jsonSchema": {
                "source": "json_schema",
                "validators": [JsonSchemaValidator()],
            },
            "createdAt": {"source": "created_at", "read_only": True},
            "modifiedAt": {"source": "modified_at", "read_only": True},
            "publishedAt": {"source": "published_at", "read_only": True},
        }
        validators = [VersionUpdateValidator()]

    def validate(self, attrs):
        valid_attrs = super().validate(attrs)

        # check parent url
        kwargs = self.context["request"].resolver_match.kwargs
        if not ObjectType.objects.filter(uuid=kwargs["objecttype_uuid"]).exists():
            msg = _("Objecttype url is invalid")
            raise serializers.ValidationError(msg, code="invalid-objecttype")

        return valid_attrs

    def create(self, validated_data):
        kwargs = self.context["request"].resolver_match.kwargs
        object_type = ObjectType.objects.get(uuid=kwargs["objecttype_uuid"])
        validated_data["object_type"] = object_type

        return super().create(validated_data)


@extend_schema_field(
    {
        "type": "object",
        "additionalProperties": {"type": "string"},
    }
)
class LabelsField(serializers.JSONField):
    pass


class ObjectTypeSerializer(serializers.HyperlinkedModelSerializer):
    labels = LabelsField(
        required=False,
        help_text=get_help_text("core.ObjectType", "labels"),
    )

    versions = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        lookup_field="version",
        view_name="objectversion-detail",
        parent_lookup_kwargs={"objecttype_uuid": "object_type__uuid"},
        help_text=_("list of URLs for the OBJECTTYPE versions"),
    )

    class Meta:
        model = ObjectType
        fields = (
            "url",
            "uuid",
            "name",
            "namePlural",
            "description",
            "dataClassification",
            "maintainerOrganization",
            "maintainerDepartment",
            "contactPerson",
            "contactEmail",
            "source",
            "updateFrequency",
            "providerOrganization",
            "documentationUrl",
            "labels",
            "createdAt",
            "modifiedAt",
            "allowGeometry",
            "versions",
        )
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "uuid": {"validators": [IsImmutableValidator()]},
            "namePlural": {"source": "name_plural"},
            "dataClassification": {"source": "data_classification"},
            "maintainerOrganization": {"source": "maintainer_organization"},
            "maintainerDepartment": {"source": "maintainer_department"},
            "contactPerson": {"source": "contact_person"},
            "contactEmail": {"source": "contact_email"},
            "updateFrequency": {"source": "update_frequency"},
            "providerOrganization": {"source": "provider_organization"},
            "documentationUrl": {"source": "documentation_url"},
            "allowGeometry": {"source": "allow_geometry"},
            "createdAt": {"source": "created_at", "read_only": True},
            "modifiedAt": {"source": "modified_at", "read_only": True},
        }
