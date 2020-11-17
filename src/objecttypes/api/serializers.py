from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from objecttypes.core.models import ObjectType, ObjectVersion


class ObjectVersionSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {"objecttype_uuid": "object_type__uuid"}

    class Meta:
        model = ObjectVersion
        fields = (
            "url",
            "version",
            "objectType",
            "publicationDate",
            "status",
            "jsonSchema",
        )
        extra_kwargs = {
            "url": {"lookup_field": "version"},
            "version": {"read_only": True},
            "objectType": {
                "source": "object_type",
                "lookup_field": "uuid",
                "read_only": True,
            },
            "publicationDate": {"source": "publication_date", "read_only": True},
            "jsonSchema": {"source": "json_schema"},
            "status": {"read_only": True},
        }


class ObjectTypeSerializer(serializers.HyperlinkedModelSerializer):
    versions = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        lookup_field="version",
        view_name="objectversion-detail",
        parent_lookup_kwargs={"objecttype_uuid": "object_type__uuid"},
    )

    class Meta:
        model = ObjectType
        fields = (
            "url",
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
            "versions",
        )
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "namePlural": {"source": "name_plural"},
            "dataClassification": {"source": "data_classification"},
            "maintainerOrganization": {"source": "maintainer_organization"},
            "maintainerDepartment": {"source": "maintainer_department"},
            "contactPerson": {"source": "contact_person"},
            "contactEmail": {"source": "contact_email"},
            "updateFrequency": {"source": "update_frequency"},
            "providerOrganization": {"source": "provider_organization"},
            "documentationUrl": {"source": "documentation_url"},
        }
