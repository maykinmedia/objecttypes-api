from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import reverse

import requests
from django_setup_configuration.configuration import BaseConfigurationStep
from django_setup_configuration.exceptions import SelfTestFailed

from objecttypes.utils import build_absolute_url


class SiteConfigurationStep(BaseConfigurationStep):
    """
    Configure the application site/domain.
    """

    verbose_name = "Site Configuration"
    required_settings = ["OBJECTTYPES_DOMAIN", "OBJECTTYPES_ORGANIZATION"]
    enable_setting = "SITES_CONFIG_ENABLE"

    def is_configured(self) -> bool:
        site = Site.objects.get_current()
        return site.domain == settings.OBJECTTYPES_DOMAIN

    def configure(self):
        site = Site.objects.get_current()
        site.domain = settings.OBJECTTYPES_DOMAIN
        site.name = f"Objecttypes {settings.OBJECTTYPES_ORGANIZATION}".strip()
        site.save()

    def test_configuration(self):
        full_url = build_absolute_url(reverse("home"))
        try:
            response = requests.get(full_url)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise SelfTestFailed(f"Could not access home page at '{full_url}'") from exc
