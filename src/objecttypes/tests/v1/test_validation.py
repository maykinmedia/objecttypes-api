import uuid

from rest_framework import status
from rest_framework.test import APITestCase

from objecttypes.core.constants import ObjectVersionStatus
from objecttypes.core.tests.factories import ObjectTypeFactory, ObjectVersionFactory
from objecttypes.utils.test import TokenAuthMixin

from .utils import reverse


class ObjectTypeValidationTests(TokenAuthMixin, APITestCase):
    def test_patch_objecttype_with_uuid_fail(self):
        object_type = ObjectTypeFactory.create()
        url = reverse("objecttype-detail", args=[object_type.uuid])

        response = self.client.patch(url, {"uuid": uuid.uuid4()})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(data["uuid"], ["This field can't be changed"])

    def test_delete_objecttype_with_versions_fail(self):
        object_type = ObjectTypeFactory.create()
        ObjectVersionFactory.create(object_type=object_type)
        url = reverse("objecttype-detail", args=[object_type.uuid])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(
            data["non_field_errors"],
            [
                "All related versions should be destroyed before destroying the objecttype"
            ],
        )


class ObjectVersionValidationTests(TokenAuthMixin, APITestCase):
    def test_create_version_with_incorrect_schema_fail(self):
        object_type = ObjectTypeFactory.create()
        url = reverse("objectversion-list", args=[object_type.uuid])
        data = {
            "jsonSchema": {
                "title": "Tree",
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "any",
            }
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("jsonSchema" in response.json())

    def test_create_version_with_incorrect_objecttype_fail(self):
        url = reverse("objectversion-list", args=[uuid.uuid4()])
        data = {
            "jsonSchema": {
                "title": "Tree",
                "$schema": "http://json-schema.org/draft-07/schema#",
                "properties": {
                    "diameter": {"type": "integer", "description": "size in cm."}
                },
            }
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["non_field_errors"], ["Objecttype url is invalid"]
        )

    def test_update_published_version_fail(self):
        object_type = ObjectTypeFactory.create()
        object_version = ObjectVersionFactory.create(
            object_type=object_type, status=ObjectVersionStatus.published
        )
        url = reverse(
            "objectversion-detail", args=[object_type.uuid, object_version.version]
        )
        new_json_schema = {
            "type": "object",
            "title": "Tree",
            "$schema": "http://json-schema.org/draft-07/schema#",
            "required": ["diameter"],
            "properties": {"diameter": {"type": "number"}},
        }

        response = self.client.put(url, {"jsonSchema": new_json_schema})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(
            data["non_field_errors"], ["Only draft versions can be changed"]
        )

    def test_delete_puclished_version_fail(self):
        object_type = ObjectTypeFactory.create()
        object_version = ObjectVersionFactory.create(
            object_type=object_type, status=ObjectVersionStatus.published
        )
        url = reverse(
            "objectversion-detail", args=[object_type.uuid, object_version.version]
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(
            data["non_field_errors"], ["Only draft versions can be destroyed"]
        )
