from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from objecttypes.core.tests.factories import ObjectTypeFactory


class AuthTests(APITestCase):
    def test_non_auth(self):
        object_type = ObjectTypeFactory.create()

        urls = [
            reverse("objecttype-list"),
            reverse("objecttype-detail", args=[object_type.uuid]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
