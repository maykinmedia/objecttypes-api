from datetime import date

from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from objecttypes.core.constants import ObjectVersionStatus
from objecttypes.core.models import ObjectVersion
from objecttypes.core.tests.factories import ObjectTypeFactory, ObjectVersionFactory
from objecttypes.utils.test import TokenAuthMixin

from .utils import reverse

JSON_SCHEMA = {
    "type": "object",
    "title": "Tree",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "required": ["diameter"],
    "properties": {"diameter": {"type": "integer", "description": "size in cm."}},
}


@freeze_time("2020-01-01")
class ObjectVersionAPITests(TokenAuthMixin, APITestCase):
    def test_get_versions(self):
        object_type = ObjectTypeFactory.create()
        object_version = ObjectVersionFactory.create(object_type=object_type)
        url = reverse("objectversion-list", args=[object_type.uuid])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "url": f"http://testserver{reverse('objectversion-detail', args=[object_type.uuid, object_version.version])}",
                        "version": object_version.version,
                        "objectType": f"http://testserver{reverse('objecttype-detail', args=[object_version.object_type.uuid])}",
                        "status": object_version.status,
                        "createdAt": "2020-01-01",
                        "modifiedAt": "2020-01-01",
                        "publishedAt": None,
                        "jsonSchema": JSON_SCHEMA,
                    }
                ],
            },
        )

    def test_get_versions_incorrect_format_uuid(self):
        """
        Regression test for https://github.com/maykinmedia/objects-api/issues/361
        """
        url = reverse("objectversion-list", args=["aaa"])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_version(self):
        object_type = ObjectTypeFactory.create()
        data = {"jsonSchema": JSON_SCHEMA, "status": ObjectVersionStatus.published}
        url = reverse("objectversion-list", args=[object_type.uuid])

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ObjectVersion.objects.count(), 1)

        object_version = ObjectVersion.objects.get()

        self.assertEqual(object_version.object_type, object_type)
        self.assertEqual(object_version.json_schema, JSON_SCHEMA)
        self.assertEqual(object_version.version, 1)
        self.assertEqual(object_version.status, ObjectVersionStatus.published)
        self.assertEqual(object_version.created_at, date(2020, 1, 1))
        self.assertEqual(object_version.modified_at, date(2020, 1, 1))
        self.assertEqual(object_version.published_at, date(2020, 1, 1))

    def test_update_version(self):
        object_type = ObjectTypeFactory.create()
        object_version = ObjectVersionFactory.create(object_type=object_type)
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

        response = self.client.put(
            url,
            {"jsonSchema": new_json_schema, "status": ObjectVersionStatus.published},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        object_version.refresh_from_db()

        self.assertEqual(object_version.json_schema, new_json_schema)
        self.assertEqual(object_version.status, ObjectVersionStatus.published)
        self.assertEqual(object_version.published_at, date(2020, 1, 1))

    def test_delete_version(self):
        object_type = ObjectTypeFactory.create()
        object_version = ObjectVersionFactory.create(object_type=object_type)
        url = reverse(
            "objectversion-detail", args=[object_type.uuid, object_version.version]
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ObjectVersion.objects.count(), 0)
