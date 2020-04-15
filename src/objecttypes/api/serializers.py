from django.db import transaction

from rest_framework import serializers

from .models import ObjectType, ObjectVersion


class ObjectVersionSerializer(serializers.ModelSerializer):
    model = ObjectVersion
    fields = ("version", "publication_date", "json_schema")


class ObjectTypeSerializer(serializers.HyperlinkedModelSerializer):
    versions = ObjectVersionSerializer(many=True)

    class Meta:
        model = ObjectType
        fields = ("url", "name", "name_plural", "versions")
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
        }

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
