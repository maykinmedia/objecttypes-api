from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from objecttypes.token.models import TokenAuth


class TestTokenAuthAuthorization(APITestCase):
    def test_valid_token(self):
        token_auth = TokenAuth.objects.create(
            contact_person="test_person",
            email="test_person@gmail.nl",
            identifier="token-1",
        )
        response = self.client.get(
            reverse("v2:objecttype-list"),
            HTTP_AUTHORIZATION=f"Token {token_auth.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_token(self):
        response = self.client.get(
            reverse("v2:objecttype-list"),
            HTTP_AUTHORIZATION=f"Token 1234-Token-5678",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_empty_token(self):
        response = self.client.get(
            reverse("v2:objecttype-list"), HTTP_AUTHORIZATION=f"Token"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_token(self):
        response = self.client.get(reverse("v2:objecttype-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
