from django.contrib.sites.models import Site

from django_setup_configuration.models import ConfigurationModel
from pydantic import Field

from objecttypes.token.models import TokenAuth


class TokenAuthConfigurationModel(ConfigurationModel):
    class Meta:
        django_model_refs = {
            TokenAuth: (
                "identifier",
                "token",
                "contact_person",
                "email",
                "organization",
                "application",
                "administration",
            )
        }


class TokenAuthGroupConfigurationModel(ConfigurationModel):
    items: list[TokenAuthConfigurationModel] = Field()


class SiteConfigurationModel(ConfigurationModel):
    class Meta:
        django_model_refs = {
            Site: (
                "domain",
                "name",
            )
        }


class SiteGroupConfigurationModel(ConfigurationModel):
    items: list[SiteConfigurationModel] = Field()
