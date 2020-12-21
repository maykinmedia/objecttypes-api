from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from objecttypes.core.tests.factories import ObjectTypeFactory
from objecttypes.token.models import TokenAuth


class AuthTests(APITestCase):
    def setUp(self) -> None:
        object_type = ObjectTypeFactory.create()
        self.urls = [
            reverse("objecttype-list"),
            reverse("objecttype-detail", args=[object_type.uuid]),
        ]

    def test_non_auth(self):
        for url in self.urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token(self):
        TokenAuth.objects.create(contact_person="John Smith", email="smith@bomen.nl")
        for url in self.urls:
            with self.subTest(url=url):
                response = self.client.get(url, HTTP_AUTHORIZATION=f"Token 12345")
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_token(self):
        token_auth = TokenAuth.objects.create(
            contact_person="John Smith", email="smith@bomen.nl"
        )
        for url in self.urls:
            with self.subTest(url=url):
                response = self.client.get(
                    url, HTTP_AUTHORIZATION=f"Token {token_auth.token}"
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)
