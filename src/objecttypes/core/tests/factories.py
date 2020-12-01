import factory

from objecttypes.core.models import ObjectType, ObjectVersion


class ObjectTypeFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")
    name_plural = factory.LazyAttribute(lambda x: "{}s".format(x.name))
    description = factory.Faker("bs")

    class Meta:
        model = ObjectType


class ObjectVersionFactory(factory.django.DjangoModelFactory):
    object_type = factory.SubFactory(ObjectTypeFactory)
    json_schema = {
        "type": "object",
        "title": "Tree",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "required": ["diameter"],
        "properties": {"diameter": {"type": "integer", "description": "size in cm."}},
    }

    class Meta:
        model = ObjectVersion
