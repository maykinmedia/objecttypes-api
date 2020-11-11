from rest_framework import serializers

from objecttypes.core.models import ObjectType, ObjectVersion


class ObjectVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectVersion
        fields = (
            "version",
            "publicationDate",
            "status",
            "jsonSchema",
        )
        extra_kwargs = {
            "publicationDate": {"source": "publication_date"},
            "jsonSchema": {"source": "json_schema"},
            "status": {"read_only": True},
        }


class ObjectTypeSerializer(serializers.HyperlinkedModelSerializer):
    versions = ObjectVersionSerializer(many=True)

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
