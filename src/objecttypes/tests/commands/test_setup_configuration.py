from io import StringIO

from django.contrib.sites.models import Site
from django.core.management import CommandError, call_command
from django.test import TestCase, override_settings
from django.urls import reverse

import requests_mock
from rest_framework import status

from objecttypes.config.demo import DemoUserStep
from objecttypes.config.objects import ObjectsAuthStep
from objecttypes.config.site import SiteConfigurationStep


@override_settings(
    OBJECTTYPES_DOMAIN="objecttypes.example.com",
    OBJECTTYPES_ORGANIZATION="ACME",
    OBJECTS_OBJECTTYPES_TOKEN="some-random-string",
    OBJECTS_OBJECTTYPES_PERSON="Some Person",
    OBJECTS_OBJECTTYPES_EMAIL="objects@objects.local",
    DEMO_CONFIG_ENABLE=True,
    DEMO_TOKEN="demo-random-string",
    DEMO_PERSON="Demo",
    DEMO_EMAIL="demo@demo.local",
)
class SetupConfigurationTests(TestCase):
    def setUp(self):
        super().setUp()

        self.addCleanup(Site.objects.clear_cache)

    @requests_mock.Mocker()
    def test_setup_configuration(self, m):
        stdout = StringIO()
        # mocks
        m.get("http://objecttypes.example.com/", status_code=200)
        m.get("http://objecttypes.example.com/api/v2/objecttypes", json=[])

        call_command("setup_configuration", stdout=stdout)

        with self.subTest("Command output"):
            command_output = stdout.getvalue().splitlines()
            expected_output = [
                f"Configuration will be set up with following steps: [{SiteConfigurationStep()}, "
                f"{ObjectsAuthStep()}, {DemoUserStep()}]",
                f"Configuring {SiteConfigurationStep()}...",
                f"{SiteConfigurationStep()} is successfully configured",
                f"Configuring {ObjectsAuthStep()}...",
                f"{ObjectsAuthStep()} is successfully configured",
                f"Configuring {DemoUserStep()}...",
                f"{DemoUserStep()} is successfully configured",
                "Instance configuration completed.",
            ]

            self.assertEqual(command_output, expected_output)

        with self.subTest("Site configured correctly"):
            site = Site.objects.get_current()
            self.assertEqual(site.domain, "objecttypes.example.com")
            self.assertEqual(site.name, "Objecttypes ACME")

        with self.subTest("Objects can query Objecttypes API"):
            response = self.client.get(
                reverse("v2:objecttype-list"),
                HTTP_AUTHORIZATION="Token some-random-string",
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.subTest("Demo user configured correctly"):
            response = self.client.get(
                reverse("v2:objecttype-list"),
                HTTP_AUTHORIZATION="Token demo-random-string",
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

    @requests_mock.Mocker()
    def test_setup_configuration_selftest_fails(self, m):
        m.get("http://objecttypes.example.com/", status_code=200)
        m.get("http://objecttypes.example.com/api/v2/objecttypes", status_code=500)

        with self.assertRaisesMessage(
            CommandError,
            "Configuration test failed with errors: "
            "Objects API Authentication Configuration: "
            "Could not list objecttypes for the configured token",
        ):
            call_command("setup_configuration")

    @requests_mock.Mocker()
    def test_setup_configuration_without_selftest(self, m):
        stdout = StringIO()

        call_command("setup_configuration", no_selftest=True, stdout=stdout)
        command_output = stdout.getvalue()

        self.assertEqual(len(m.request_history), 0)
        self.assertTrue("Selftest is skipped" in command_output)
