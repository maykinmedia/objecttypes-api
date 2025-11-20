from unittest.mock import MagicMock, patch

from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from objecttypes.api.metrics import (
    objecttype_create_counter,
    objecttype_delete_counter,
    objecttype_update_counter,
)
from objecttypes.core.tests.factories import ObjectTypeFactory
from objecttypes.utils.test import TokenAuthMixin

from .utils import reverse


@freeze_time("2020-01-01")
class ObjectTypeMetricTests(TokenAuthMixin, APITestCase):
    @patch.object(objecttype_create_counter, "add", wraps=objecttype_create_counter.add)
    def test_objecttype_create_counter(self, mock_add: MagicMock):
        url = reverse("objecttype-list")

        response = self.client.post(
            url,
            {
                "name": "Boom",
                "namePlural": "Bomen",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        mock_add.assert_called_once_with(1)

    @patch.object(objecttype_update_counter, "add", wraps=objecttype_update_counter.add)
    def test_objecttype_update_counter(self, mock_add: MagicMock):
        obj = ObjectTypeFactory.create()
        url = reverse("objecttype-detail", args=[obj.uuid])

        response = self.client.patch(url, {"name": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        mock_add.assert_called_once_with(1)

    @patch.object(objecttype_delete_counter, "add", wraps=objecttype_delete_counter.add)
    def test_objecttype_delete_counter(self, mock_add: MagicMock):
        obj = ObjectTypeFactory.create()
        url = reverse("objecttype-detail", args=[obj.uuid])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        mock_add.assert_called_once_with(1)
