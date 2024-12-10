from pathlib import Path

from django.contrib.sites.models import Site
from django.test import TestCase

from django_setup_configuration.exceptions import PrerequisiteFailed
from django_setup_configuration.test_utils import execute_single_step

from objecttypes.setup_configuration.steps import SitesConfigurationStep

DIR_FILES = (Path(__file__).parent / "files/sites").resolve()


class SitesConfigurationStepTests(TestCase):
    def test_valid_setup_default(self):
        self.assertEqual(Site.objects.count(), 1)
        
        site = Site.objects.get(name="example.com")
        self.assertEqual(site.domain, "example.com")
        self.assertEqual(site.name, "example.com")

        execute_single_step(
            SitesConfigurationStep, yaml_source=str(DIR_FILES / "valid_setup.yaml")
        )

        sites = Site.objects.order_by("pk")
        self.assertEqual(sites.count(), 3)

        site = sites.get(name="example-1")
        self.assertEqual(site.domain, "example-1.com")
        self.assertEqual(site.name, "example-1")

        site = sites.get(name="example-2")
        self.assertEqual(site.domain, "example-2.com")
        self.assertEqual(site.name, "example-2")

    def test_valid_update_existing_sites(self):
        self.assertEqual(Site.objects.count(), 1)

        site = Site.objects.get(name="example.com")
        self.assertEqual(site.domain, "example.com")
        self.assertEqual(site.name, "example.com")

        Site.objects.create(domain="example-2.com", name="example-3")
        sites = Site.objects.order_by("pk")
        self.assertEqual(sites.count(), 2)

        execute_single_step(
            SitesConfigurationStep, yaml_source=str(DIR_FILES / "valid_setup.yaml")
        )

        sites = Site.objects.order_by("pk")
        self.assertEqual(sites.count(), 3)

        site = sites.get(name="example-2")
        self.assertEqual(site.domain, "example-2.com")
        self.assertEqual(site.name, "example-2")

        site = sites.get(name="example-1")
        self.assertEqual(site.domain, "example-1.com")
        self.assertEqual(site.name, "example-1")

    def test_invalid_setup_empty(self):
        self.assertEqual(Site.objects.count(), 1)
        
        site = Site.objects.get(name="example.com")
        self.assertEqual(site.domain, "example.com")
        self.assertEqual(site.name, "example.com")

        with self.assertRaises(PrerequisiteFailed) as command_error:
            execute_single_step(
                SitesConfigurationStep,
                yaml_source=str(DIR_FILES / "invalid_setup.yaml"),
            )

        self.assertTrue("Input should be a valid list" in str(command_error.exception))

        self.assertEqual(Site.objects.count(), 1)
        
        site = Site.objects.get(name="example.com")
        self.assertEqual(site.domain, "example.com")
        self.assertEqual(site.name, "example.com")
