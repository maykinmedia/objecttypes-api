import json
from datetime import date

from django.urls import reverse_lazy

from django_webtest import WebTest

from objecttypes.accounts.models import User
from objecttypes.core.constants import ObjectVersionStatus
from objecttypes.core.models import ObjectType

JSON_SCHEMA = {
    "type": "object",
    "title": "Tree",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "required": ["diameter"],
    "properties": {"diameter": {"type": "integer", "description": "size in cm."}},
}


class AdminAddTests(WebTest):
    url = reverse_lazy("admin:core_objecttype_add")

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.user = User.objects.create_superuser(
            "test_user", "test_user@test.nl", "test"
        )

    def setUp(self) -> None:
        super().setUp()

        self.app.set_user(self.user)

    def test_create_objecttype_success(self):
        get_response = self.app.get(self.url)

        form = get_response.form
        form["name"] = "boom"
        form["name_plural"] = "bomen"
        form["description"] = "some object type description"
        form["public"] = False
        form["maintainer"] = "tree municipality"
        form["contact"] = "John Smith"
        form["domain"] = "object types department"
        form["versions-0-publication_date"] = date(2020, 1, 1)
        form["versions-0-json_schema"] = json.dumps(JSON_SCHEMA)

        response = form.submit()

        # redirect on successful create, 200 on validation errors, 500 on db errors
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ObjectType.objects.count(), 1)

        object_type = ObjectType.objects.get()

        self.assertEqual(object_type.name, "boom")
        self.assertEqual(object_type.name_plural, "bomen")
        self.assertEqual(object_type.description, "some object type description")
        self.assertEqual(object_type.public, False)
        self.assertEqual(object_type.maintainer, "tree municipality")
        self.assertEqual(object_type.contact, "John Smith")
        self.assertEqual(object_type.domain, "object types department")
        self.assertEqual(object_type.versions.count(), 1)

        object_version = object_type.last_version

        self.assertEqual(object_version.version, 1)
        self.assertEqual(object_version.publication_date, date(2020, 1, 1))
        self.assertEqual(object_version.json_schema, JSON_SCHEMA)
        self.assertEqual(object_version.status, ObjectVersionStatus.draft)

    def test_create_objecttype_without_version_fail(self):
        get_response = self.app.get(self.url)

        form = get_response.form
        form["name"] = "boom"
        form["name_plural"] = "bomen"
        form["description"] = "some object type description"
        form["public"] = False
        form["maintainer"] = "tree municipality"
        form["contact"] = "John Smith"
        form["domain"] = "object types department"

        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ObjectType.objects.count(), 0)

    def test_create_objecttype_with_invalid_json_schema(self):
        get_response = self.app.get(self.url)

        form = get_response.form
        form["name"] = "boom"
        form["name_plural"] = "bomen"
        form["description"] = "some object type description"
        form["public"] = False
        form["maintainer"] = "tree municipality"
        form["contact"] = "John Smith"
        form["domain"] = "object types department"
        form["versions-0-publication_date"] = date(2020, 1, 1)
        form["versions-0-json_schema"] = json.dumps(
            {
                "title": "Tree",
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "any",
            }
        )

        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ObjectType.objects.count(), 0)
