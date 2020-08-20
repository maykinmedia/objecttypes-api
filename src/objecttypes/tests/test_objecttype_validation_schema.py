from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from objecttypes.api.models import ObjectType


class ObjectTypeValidationTests(APITestCase):
    def test_create_objecttype_success(self):
        url = reverse("objecttype-list")
        data = {
            "name": "boom",
            "namePlural": "bomen",
            "description": "object type for trees",
            "versions": [
                {
                    "version": 1,
                    "publicationDate": "2020-03-01",
                    "jsonSchema": {
                        "title": "Tree",
                        "$schema": "http://json-schema.org/draft-07/schema#",
                        "type": "object",
                        "required": ["diameter"],
                        "properties": {
                            "diameter": {
                                "description": "size in cm.",
                                "type": "integer",
                            },
                            "plantDate": {
                                "type": "string",
                                "description": "the date the tree was planted.",
                            },
                        },
                    },
                }
            ],
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ObjectType.objects.count(), 1)

        object_type = ObjectType.objects.get()
        self.assertEqual(object_type.name, "boom")
        self.assertEqual(object_type.versions.count(), 1)

        object_version = object_type.versions.get()
        self.assertEqual(object_version.version, 1)
        self.assertEqual(
            object_version.json_schema,
            {
                "title": "Tree",
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object",
                "required": ["diameter"],
                "properties": {
                    "diameter": {"description": "size in cm.", "type": "integer",},
                    "plantDate": {
                        "type": "string",
                        "description": "the date the tree was planted.",
                    },
                },
            },
        )

    def test_create_objecttype_no_versions(self):
        url = reverse("objecttype-list")
        data = {
            "name": "boom",
            "namePlural": "bomen",
            "versions": [],
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ObjectType.objects.count(), 0)

        data = response.json()
        self.assertEqual(data["versions"], ["This field can't be empty"])

    def test_create_objecttype_invalid_schema(self):
        url = reverse("objecttype-list")
        data = {
            "name": "boom",
            "namePlural": "bomen",
            "versions": [
                {
                    "version": 1,
                    "publicationDate": "2020-03-01",
                    "jsonSchema": {
                        "title": "Tree",
                        "$schema": "http://json-schema.org/draft-07/schema#",
                        "type": "any",
                    },
                }
            ],
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ObjectType.objects.count(), 0)

        data = response.json()
        self.assertEqual(
            data["versions"],
            [{"jsonSchema": ["'any' is not valid under any of the given schemas"]}],
        )
