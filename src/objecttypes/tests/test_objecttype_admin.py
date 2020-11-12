import json
from datetime import date

from django.urls import reverse, reverse_lazy

from django_webtest import WebTest
from freezegun import freeze_time

from objecttypes.accounts.tests.factories import SuperUserFactory
from objecttypes.core.constants import (
    DataClassificationChoices,
    ObjectVersionStatus,
    UpdateFrequencyChoices,
)
from objecttypes.core.models import ObjectType
from objecttypes.core.tests.factories import ObjectTypeFactory, ObjectVersionFactory

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

        cls.user = SuperUserFactory.create()

    def setUp(self) -> None:
        super().setUp()

        self.app.set_user(self.user)

    def test_create_objecttype_success(self):
        get_response = self.app.get(self.url)

        form = get_response.form
        form["name"] = "boom"
        form["name_plural"] = "bomen"
        form["description"] = "some object type description"
        form["data_classification"] = DataClassificationChoices.intern
        form["maintainer_organization"] = "tree municipality"
        form["maintainer_department"] = "object types department"
        form["contact_person"] = "John Smith"
        form["contact_email"] = "John.Smith@objecttypes.nl"
        form["source"] = "tree system"
        form["update_frequency"] = UpdateFrequencyChoices.monthly
        form["provider_organization"] = "tree provider"
        form["documentation_url"] = "http://example.com/doc/trees"
        form["labels"] = json.dumps({"key1": "value1"})

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
        self.assertEqual(
            object_type.data_classification, DataClassificationChoices.intern
        )
        self.assertEqual(object_type.maintainer_organization, "tree municipality")
        self.assertEqual(object_type.maintainer_department, "object types department")
        self.assertEqual(object_type.contact_person, "John Smith")
        self.assertEqual(object_type.contact_email, "John.Smith@objecttypes.nl")
        self.assertEqual(object_type.source, "tree system")
        self.assertEqual(object_type.update_frequency, UpdateFrequencyChoices.monthly)
        self.assertEqual(object_type.provider_organization, "tree provider")
        self.assertEqual(object_type.documentation_url, "http://example.com/doc/trees")
        self.assertEqual(object_type.labels, {"key1": "value1"})
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
        form["maintainer_organization"] = "tree municipality"

        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ObjectType.objects.count(), 0)

    def test_create_objecttype_with_invalid_json_schema(self):
        get_response = self.app.get(self.url)

        form = get_response.form
        form["name"] = "boom"
        form["name_plural"] = "bomen"
        form["description"] = "some object type description"
        form["maintainer_organization"] = "tree municipality"
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


class AdminDetailTests(WebTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.user = SuperUserFactory.create()

    def setUp(self) -> None:
        super().setUp()

        self.app.set_user(self.user)

    def test_display_only_last_version(self):
        object_type = ObjectTypeFactory.create()
        ObjectVersionFactory.create_batch(3, object_type=object_type)
        url = reverse("admin:core_objecttype_change", args=[object_type.id])

        get_response = self.app.get(url)
        form = get_response.form

        self.assertEqual(int(form["versions-TOTAL_FORMS"].value), 1)
        self.assertEqual(int(form["versions-0-id"].value), object_type.last_version.id)

    def test_update_draft(self):
        object_type = ObjectTypeFactory.create()
        object_version = ObjectVersionFactory.create(object_type=object_type)
        url = reverse("admin:core_objecttype_change", args=[object_type.id])

        get_response = self.app.get(url)

        save_button = get_response.html.find("input", {"name": "_save"})
        self.assertIsNotNone(save_button)

        form = get_response.form
        form["versions-0-publication_date"] = date(2020, 1, 1)
        response = form.submit()

        self.assertEqual(response.status_code, 302)

        object_version.refresh_from_db()
        self.assertEqual(object_version.publication_date, date(2020, 1, 1))

    def test_update_published_no_buttons(self):
        object_type = ObjectTypeFactory.create()
        ObjectVersionFactory.create(
            object_type=object_type, status=ObjectVersionStatus.published
        )
        url = reverse("admin:core_objecttype_change", args=[object_type.id])

        get_response = self.app.get(url)

        save_button = get_response.html.find("input", {"name": "_save"})
        self.assertIsNone(save_button)

    def test_publish_draft(self):
        object_type = ObjectTypeFactory.create()
        object_version = ObjectVersionFactory.create(object_type=object_type)
        url = reverse("admin:core_objecttype_change", args=[object_type.id])

        get_response = self.app.get(url)

        publish_button = get_response.html.find("input", {"name": "_publish"})
        self.assertIsNotNone(publish_button)

        form = get_response.form
        response = form.submit("_publish")

        self.assertEqual(response.status_code, 302)

        object_version.refresh_from_db()
        self.assertEqual(object_version.status, ObjectVersionStatus.published)

    def test_publish_published_no_button(self):
        object_type = ObjectTypeFactory.create()
        ObjectVersionFactory.create(
            object_type=object_type, status=ObjectVersionStatus.published
        )
        url = reverse("admin:core_objecttype_change", args=[object_type.id])

        get_response = self.app.get(url)

        publish_button = get_response.html.find("input", {"name": "_publish"})
        self.assertIsNone(publish_button)

    def test_new_version_draft_no_button(self):
        object_type = ObjectTypeFactory.create()
        ObjectVersionFactory.create(object_type=object_type)
        url = reverse("admin:core_objecttype_change", args=[object_type.id])

        get_response = self.app.get(url)

        new_version_button = get_response.html.find("input", {"name": "_newversion"})
        self.assertIsNone(new_version_button)

    @freeze_time("2020-02-02")
    def test_new_version_published(self):
        object_type = ObjectTypeFactory.create()
        object_version = ObjectVersionFactory.create(
            object_type=object_type, status=ObjectVersionStatus.published
        )
        url = reverse("admin:core_objecttype_change", args=[object_type.id])

        get_response = self.app.get(url)

        new_version_button = get_response.html.find("input", {"name": "_newversion"})
        self.assertIsNotNone(new_version_button)

        form = get_response.form
        response = form.submit("_newversion")

        self.assertEqual(response.status_code, 302)

        object_type.refresh_from_db()
        self.assertEqual(object_type.versions.count(), 2)

        last_version = object_type.last_version
        self.assertNotEqual(last_version, object_version)
        self.assertEqual(last_version.version, object_version.version + 1)
        self.assertEqual(last_version.json_schema, object_version.json_schema)
        self.assertEqual(last_version.publication_date, date(2020, 2, 2))
        self.assertEqual(last_version.status, ObjectVersionStatus.draft)

    def test_display_all_versions_in_history(self):
        object_type = ObjectTypeFactory.create()
        ObjectVersionFactory.create_batch(3, object_type=object_type)
        url = reverse("admin:core_objecttype_history", args=[object_type.id])

        response = self.app.get(url)

        self.assertEqual(response.status_code, 200)

        table = response.html.find(id="change-history")
        table_rows = table.tbody.find_all("tr")

        self.assertEqual(len(table_rows), 3)

        for object_version, row in zip(object_type.ordered_versions, table_rows):
            row_version, row_status, row_schema = row.find_all("td")
            self.assertEqual(int(row_version.text), object_version.version)
            self.assertEqual(row_status.text, object_version.get_status_display())
            self.assertEqual(
                json.loads(row_schema.text.replace("'", '"')),
                object_version.json_schema,
            )
