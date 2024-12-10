from pathlib import Path

from django.contrib.sites.models import Site
from django.test import TestCase

from django_setup_configuration.exceptions import PrerequisiteFailed
from django_setup_configuration.test_utils import execute_single_step

from objecttypes.setup_configuration.steps import SitesConfigurationStep

DIR_FILES = (Path(__file__).parent / "files/sites").resolve()


class SitesConfigurationStepTests(TestCase):
    def test_valid_setup_default(self):
        self.assertTrue(Site.objects.filter(domain="example.com", name="example.com").exists())

        execute_single_step(
            SitesConfigurationStep, yaml_source=str(DIR_FILES / "valid_setup.yaml")
        )

        sites = Site.objects.all()
        self.assertEqual(sites.count(), 3)
        self.assertTrue(sites.filter(domain="example-1.com", name="example-1").exists())
        self.assertTrue(sites.filter(domain="example-2.com", name="example-2").exists())

    def test_valid_update_existing_sites(self):
        self.assertTrue(Site.objects.filter(domain="example.com", name="example.com").exists())

        Site.objects.create(domain="example-2.com", name="example-3")
        self.assertEqual(Site.objects.count(), 2)

        execute_single_step(
            SitesConfigurationStep, yaml_source=str(DIR_FILES / "valid_setup.yaml")
        )

        sites = Site.objects.all()
        self.assertEqual(sites.count(), 3)
        self.assertTrue(sites.filter(domain="example-2.com", name="example-2").exists())
        self.assertTrue(sites.filter(domain="example-1.com", name="example-1").exists())

    def test_invalid_setup_empty(self):
        self.assertTrue(Site.objects.filter(domain="example.com", name="example.com").exists())

        with self.assertRaises(PrerequisiteFailed) as command_error:
            execute_single_step(
                SitesConfigurationStep,
                yaml_source=str(DIR_FILES / "invalid_setup.yaml"),
            )

        self.assertTrue("Input should be a valid list" in str(command_error.exception))
        self.assertEqual(Site.objects.count(), 1)
