from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from objecttypes.core.tests.factories import ObjectTypeFactory, ObjectVersionFactory
from objecttypes.utils.test import TokenAuthMixin


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
                    {
                        "version": object_version.version,
                        "publicationDate": object_version.publication_date.isoformat(),
                        "jsonSchema": object_version.json_schema,
                        "status": object_version.status,
                    }
                ],
            },
        )
