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
    version = factory.Sequence(lambda n: n)
    json_schema = {
        "title": "schema",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "any",
    }

    class Meta:
        model = ObjectVersion
