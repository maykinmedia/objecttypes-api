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
            "publicData",
            "maintainerOrganization",
            "maintainerDepartment",
            "contactEmail",
            "versions",
        )
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "namePlural": {"source": "name_plural"},
            "publicData": {"source": "public_data"},
            "maintainerOrganization": {"source": "maintainer_organization"},
            "maintainerDepartment": {"source": "maintainer_department"},
            "contactEmail": {"source": "contact_email"},
        }
