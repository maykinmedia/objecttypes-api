from datetime import date

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from objecttypes.core.constants import (
    DataClassificationChoices,
    ObjectVersionStatus,
    UpdateFrequencyChoices,
)
from objecttypes.core.models import ObjectType, ObjectVersion
from objecttypes.core.tests.factories import ObjectTypeFactory, ObjectVersionFactory
from objecttypes.utils.test import TokenAuthMixin

JSON_SCHEMA = {
    "type": "object",
    "title": "Tree",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "required": ["diameter"],
    "properties": {"diameter": {"type": "integer", "description": "size in cm."}},
}


class ObjectTypeAPITests(TokenAuthMixin, APITestCase):
    def test_get_objecttypes(self):
        object_type = ObjectTypeFactory.create()
        object_version = ObjectVersionFactory.create(object_type=object_type)
        url = reverse("objecttype-detail", args=[object_type.uuid])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "url": f"http://testserver{url}",
                "name": object_type.name,
                "namePlural": object_type.name_plural,
                "description": object_type.description,
                "dataClassification": object_type.data_classification,
                "maintainerOrganization": object_type.maintainer_organization,
                "maintainerDepartment": object_type.maintainer_department,
                "contactPerson": object_type.contact_person,
                "contactEmail": object_type.contact_email,
                "source": object_type.source,
                "updateFrequency": object_type.update_frequency,
                "providerOrganization": object_type.provider_organization,
                "documentationUrl": object_type.documentation_url,
                "labels": object_type.labels,
                "versions": [
                    f"http://testserver{reverse('objectversion-detail', args=[object_type.uuid, object_version.version])}"
                ],
            },
        )

    def test_create_objecttype(self):
        url = reverse("objecttype-list")
        data = {
            "name": "boom",
            "namePlural": "bomen",
            "description": "tree type description",
            "dataClassification": DataClassificationChoices.intern,
            "maintainerOrganization": "tree municipality",
            "maintainerDepartment": "object types department",
            "contactPerson": "John Smith",
            "contactEmail": "John.Smith@objecttypes.nl",
            "source": "tree system",
            "updateFrequency": UpdateFrequencyChoices.monthly,
            "providerOrganization": "tree provider",
            "documentationUrl": "http://example.com/doc/trees",
            "labels": {"key1": "value1"},
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ObjectType.objects.count(), 1)

        object_type = ObjectType.objects.get()

        self.assertEqual(object_type.name, "boom")
        self.assertEqual(object_type.name_plural, "bomen")
        self.assertEqual(object_type.description, "tree type description")
        self.assertEqual(
            object_type.data_classification, DataClassificationChoices.intern
        )
        self.assertEqual(object_type.maintainer_organization, "tree municipality")
        self.assertEqual(object_type.maintainer_department, "object types department")
        self.assertEqual(object_type.contact_person, "John Smith")
        self.assertEqual(object_type.contact_email, "John.Smith@objecttypes.nl")
        self.assertEqual(object_type.source, "tree system")
        self.assertEqual(object_type.update_frequency, UpdateFrequencyChoices.monthly)
        self.assertEqual(object_type.provider_organization, "tree provider")
        self.assertEqual(object_type.documentation_url, "http://example.com/doc/trees")
        self.assertEqual(object_type.labels, {"key1": "value1"})

    def test_update_objecttype(self):
        object_type = ObjectTypeFactory.create(
            data_classification=DataClassificationChoices.intern
        )
        url = reverse("objecttype-detail", args=[object_type.uuid])

        response = self.client.patch(
            url, {"dataClassification": DataClassificationChoices.open}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        object_type.refresh_from_db()

        self.assertEqual(
            object_type.data_classification, DataClassificationChoices.open
        )

    def test_delete_objecttype_not_supported(self):
        object_type = ObjectTypeFactory.create()
        url = reverse("objecttype-detail", args=[object_type.uuid])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ObjectVersionAPITests(TokenAuthMixin, APITestCase):
    def test_get_versions(self):
        object_type = ObjectTypeFactory.create()
        object_version = ObjectVersionFactory.create(object_type=object_type)
        url = reverse("objectversion-list", args=[object_type.uuid])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [
                {
                    "url": f"http://testserver{reverse('objectversion-detail', args=[object_type.uuid, object_version.version])}",
                    "version": object_version.version,
                    "objectType": f"http://testserver{reverse('objecttype-detail', args=[object_version.object_type.uuid])}",
                    "publicationDate": object_version.publication_date.isoformat(),
                    "status": object_version.status,
                    "jsonSchema": JSON_SCHEMA,
                }
            ],
        )

    def test_create_version(self):
        object_type = ObjectTypeFactory.create()
        data = {"jsonSchema": JSON_SCHEMA}
        url = reverse("objectversion-list", args=[object_type.uuid])

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ObjectVersion.objects.count(), 1)

        object_version = ObjectVersion.objects.get()

        self.assertEqual(object_version.object_type, object_type)
        self.assertEqual(object_version.json_schema, JSON_SCHEMA)
        self.assertEqual(object_version.version, 1)
        self.assertEqual(object_version.publication_date, date.today())
        self.assertEqual(object_version.status, ObjectVersionStatus.draft)

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

        response = self.client.put(url, {"jsonSchema": new_json_schema})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_version_not_supported(self):
        object_type = ObjectTypeFactory.create()
        object_version = ObjectVersionFactory.create(object_type=object_type)
        url = reverse(
            "objectversion-detail", args=[object_type.uuid, object_version.version]
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
