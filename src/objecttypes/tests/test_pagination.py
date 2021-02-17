from django.urls import reverse_lazy

from rest_framework import status
from rest_framework.test import APITestCase

from objecttypes.core.tests.factories import ObjectTypeFactory
from objecttypes.utils.test import TokenAuthMixin


class ObjectTypePaginationTests(TokenAuthMixin, APITestCase):
    url = reverse_lazy("objecttype-list")

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        ObjectTypeFactory.create_batch(10)

    def test_list_with_default_page_size(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["count"], 10)
        self.assertIsNone(data["next"])

    def test_list_with_page_size_in_query(self):
        response = self.client.get(self.url, {"pageSize": 5})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["count"], 10)
        self.assertEqual(data["next"], f"http://testserver{self.url}?page=2&pageSize=5")
