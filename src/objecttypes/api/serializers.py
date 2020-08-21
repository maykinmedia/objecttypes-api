from django.db import transaction

from jsonschema.exceptions import SchemaError
from jsonschema.validators import validator_for
from rest_framework import serializers

from .models import ObjectType, ObjectVersion


class ObjectVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectVersion
        fields = ("version", "publicationDate", "jsonSchema")
        extra_kwargs = {
            "publicationDate": {"source": "publication_date"},
            "jsonSchema": {"source": "json_schema"},
        }

    def validate_jsonSchema(self, schema):
        schema_validator = validator_for(schema)
        try:
            schema_validator.check_schema(schema)
        except SchemaError as exc:
            raise serializers.ValidationError(exc.args[0]) from exc

        return schema


class ObjectTypeSerializer(serializers.HyperlinkedModelSerializer):
    versions = ObjectVersionSerializer(many=True)

    class Meta:
        model = ObjectType
        fields = (
            "url",
            "name",
            "namePlural",
            "description",
            "public",
            "maintainer",
            "contact",
            "domain",
            "status",
            "versions",
        )
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "namePlural": {"source": "name_plural"},
            "status": {"read_only": True},
        }

    def validate_versions(self, value):
        # versions should always be filled
        if not value:
            raise serializers.ValidationError("This field can't be empty")

        return value

    @transaction.atomic
    def create(self, validated_data):
        versions_data = validated_data.pop("versions")
        object_type = super().create(validated_data)

        for version_data in versions_data:
            ObjectVersion.objects.create(**version_data, object_type=object_type)

        return object_type

    @transaction.atomic
    def update(self, instance, validated_data):
        versions_data = validated_data.pop("versions")
        object_type = super().update(instance, validated_data)

        # in case of update objecttype - remove all related versions first
        object_type.versions.all().delete()
        for version_data in versions_data:
            ObjectVersion.objects.create(**version_data, object_type=object_type)

        return object_type
