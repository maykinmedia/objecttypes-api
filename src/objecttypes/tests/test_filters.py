from django.urls import reverse, reverse_lazy

from rest_framework import status
from rest_framework.test import APITestCase

from objecttypes.core.tests.factories import ObjectTypeFactory


class FilterTests(APITestCase):
    url = reverse_lazy("objecttype-list")

    def test_filter_public_data(self):
        object_type_1 = ObjectTypeFactory.create(public_data=True)
        object_type_2 = ObjectTypeFactory.create(public_data=False)

        response = self.client.get(self.url, {"publicData": True})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["url"],
            f"http://testserver{reverse('objecttype-detail', args=[object_type_1.uuid])}",
        )
