from pathlib import Path

from django.contrib.sites.models import Site
from django.test import TestCase

from django_setup_configuration.exceptions import PrerequisiteFailed
from django_setup_configuration.test_utils import build_step_config_from_sources

from objecttypes.setup_configuration.steps import SitesConfigurationStep

DIR_FILES = (Path(__file__).parent / "files/sites").resolve()


class SitesConfigurationStepTests(TestCase):
    def test_valid_setup_default(self):
        sites = Site.objects.order_by("pk")
        site = sites[0]
        self.assertEqual(sites.count(), 1)
        self.assertEqual(site.domain, "example.com")
        self.assertEqual(site.name, "example.com")

        setup_config = build_step_config_from_sources(
            SitesConfigurationStep,
            str(DIR_FILES / "valid_setup.yaml"),
        )
        step = SitesConfigurationStep()
        step.execute(setup_config)

        sites = Site.objects.order_by("pk")
        self.assertEqual(sites.count(), 3)

        site = sites[1]
        self.assertEqual(site.domain, "example-1.com")
        self.assertEqual(site.name, "example-1")

        site = sites[2]
        self.assertEqual(site.domain, "example-2.com")
        self.assertEqual(site.name, "example-2")

    def test_valid_update_existing_sites(self):
        sites = Site.objects.order_by("pk")
        site = sites[0]
        self.assertEqual(sites.count(), 1)
        self.assertEqual(site.domain, "example.com")
        self.assertEqual(site.name, "example.com")

        Site.objects.create(domain="example-2.com", name="example-3")
        sites = Site.objects.order_by("pk")
        self.assertEqual(sites.count(), 2)

        setup_config = build_step_config_from_sources(
            SitesConfigurationStep,
            str(DIR_FILES / "valid_setup.yaml"),
        )
        step = SitesConfigurationStep()
        step.execute(setup_config)

        sites = Site.objects.order_by("pk")
        self.assertEqual(sites.count(), 3)

        site = sites[1]
        self.assertEqual(site.domain, "example-2.com")
        self.assertEqual(site.name, "example-2")

        site = sites[2]
        self.assertEqual(site.domain, "example-1.com")
        self.assertEqual(site.name, "example-1")

    def test_invalid_setup_empty(self):
        sites = Site.objects.order_by("pk")
        site = sites[0]
        self.assertEqual(sites.count(), 1)
        self.assertEqual(site.domain, "example.com")
        self.assertEqual(site.name, "example.com")

        with self.assertRaises(PrerequisiteFailed) as command_error:
            setup_config = build_step_config_from_sources(
                SitesConfigurationStep,
                str(DIR_FILES / "invalid_setup.yaml"),
            )
            step = SitesConfigurationStep()
            step.execute(setup_config)

        self.assertTrue("Input should be a valid list" in str(command_error.exception))

        sites = Site.objects.order_by("pk")
        site = sites[0]
        self.assertEqual(sites.count(), 1)
        self.assertEqual(site.domain, "example.com")
        self.assertEqual(site.name, "example.com")
