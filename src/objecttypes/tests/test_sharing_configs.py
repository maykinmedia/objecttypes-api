import base64
import json
from datetime import date
from unittest.mock import patch

from django.urls import reverse

import requests_mock
from django_webtest import WebTest
from freezegun import freeze_time
from maykin_2fa.test import disable_admin_mfa
from sharing_configs.models import SharingConfigsConfig

from objecttypes.accounts.tests.factories import SuperUserFactory
from objecttypes.core.constants import DataClassificationChoices, ObjectVersionStatus
from objecttypes.core.models import ObjectType
from objecttypes.core.tests.factories import ObjectTypeFactory, ObjectVersionFactory

JSON_SCHEMA = {"title": "Tree"}
SHARING_CONFIGS_API_ROOT = "https://sharing-configs-api.example.org/api/v1/"


@disable_admin_mfa()
@freeze_time("2020-01-01")
class SharingConfigsTests(WebTest):
    def setUp(self) -> None:
        super().setUp()

        config = SharingConfigsConfig.get_solo()
        config.api_endpoint = SHARING_CONFIGS_API_ROOT
        config.label = "objecttypes"
        config.api_key = "123456"
        config.save()

        self.user = SuperUserFactory.create()
        self.app.set_user(self.user)

        folder_choices_patcher = patch(
            "sharing_configs.forms.get_imported_folders_choices",
            return_value=[("example_folder", "example_folder")],
        )
        folder_choices_patcher.start()
        self.addCleanup(folder_choices_patcher.stop)

    @requests_mock.Mocker()
    def test_import_jsonschema_with_sharing_configs(self, m):
        url = reverse("admin:core_objecttype_import")
        get_response = self.app.get(url)
        self.assertEqual(get_response.status_code, 200)

        m.get(
            f"{SHARING_CONFIGS_API_ROOT}config/objecttypes/folder/example_folder/files/boom.json",
            content=json.dumps(JSON_SCHEMA).encode(),
        )

        form = get_response.form
        form["folder"] = "example_folder"
        form["file_name"].force_value("boom.json")  # ajax is used to update options

        response = form.submit()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ObjectType.objects.count(), 1)

        object_type = ObjectType.objects.get()

        self.assertEqual(object_type.name, "Tree")
        self.assertEqual(object_type.name_plural, "")
        self.assertEqual(
            object_type.data_classification, DataClassificationChoices.open
        )
        self.assertEqual(object_type.created_at, date(2020, 1, 1))
        self.assertEqual(object_type.modified_at, date(2020, 1, 1))
        self.assertEqual(object_type.versions.count(), 1)

        object_version = object_type.last_version

        self.assertEqual(object_version.version, 1)
        self.assertEqual(object_version.status, ObjectVersionStatus.draft)
        self.assertEqual(object_version.created_at, date(2020, 1, 1))
        self.assertEqual(object_version.modified_at, date(2020, 1, 1))
        self.assertIsNone(object_version.published_at)
        self.assertEqual(object_version.json_schema, JSON_SCHEMA)

    @requests_mock.Mocker()
    def test_export_jsonschema_with_sharing_configs(self, m):
        object_type = ObjectTypeFactory.create()
        object_version = ObjectVersionFactory.create(
            object_type=object_type, json_schema=JSON_SCHEMA
        )
        url = reverse("admin:core_objecttype_export", args=[object_type.id])

        get_response = self.app.get(url)
        self.assertEqual(get_response.status_code, 200)

        m.post(
            f"{SHARING_CONFIGS_API_ROOT}config/objecttypes/folder/example_folder/files/",
            json={
                "url": f"{SHARING_CONFIGS_API_ROOT}config/objecttypes/folder/example_folder/files/boom.json"
            },
        )

        form = get_response.form
        form["folder"] = "example_folder"
        form["file_name"] = "boom.json"

        response = form.submit()

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            m.last_request.url,
            f"{SHARING_CONFIGS_API_ROOT}config/objecttypes/folder/example_folder/files/",
        )
        self.assertEqual(
            m.last_request.json(),
            {
                "author": self.user.username,
                "content": base64.b64encode(
                    json.dumps(object_version.json_schema).encode()
                ).decode("utf-8"),
                "filename": "boom.json",
                "overwrite": False,
            },
        )
