from rest_framework import status
from rest_framework.test import APITestCase

from objecttypes.core.constants import DataClassificationChoices
from objecttypes.core.tests.factories import ObjectTypeFactory
from objecttypes.utils.test import TokenAuthMixin

from .utils import reverse, reverse_lazy


class FilterTests(TokenAuthMixin, APITestCase):
    url = reverse_lazy("objecttype-list")

    def test_filter_public_data(self):
        object_type_1 = ObjectTypeFactory.create(
            data_classification=DataClassificationChoices.open
        )
        ObjectTypeFactory.create(
            data_classification=DataClassificationChoices.intern
        )

        response = self.client.get(
            self.url, {"dataClassification": DataClassificationChoices.open}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["url"],
            f"http://testserver{reverse('objecttype-detail', args=[object_type_1.uuid])}",
        )
