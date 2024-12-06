import logging

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from django_setup_configuration.configuration import BaseConfigurationStep
from django_setup_configuration.exceptions import ConfigurationRunFailed

from objecttypes.setup_configuration.models import TokenAuthGroupConfigurationModel
from objecttypes.token.models import TokenAuth

logger = logging.getLogger(__name__)


class TokenAuthConfigurationStep(
    BaseConfigurationStep[TokenAuthGroupConfigurationModel]
):
    """
    Configure configuration groups for the Objects API backend
    """

    namespace = "objecttypes_tokens"
    enable_setting = "objecttypes_tokens_config_enable"

    verbose_name = "Configuration to set up authentication tokens for ObjectTypes"
    config_model = TokenAuthGroupConfigurationModel

    def execute(self, model: TokenAuthGroupConfigurationModel) -> None:
        for item in model.items:
            logger.info(f"Configuring {item.identifier}")

            model_kwargs = {
                "identifier": item.identifier,
                "token": item.token,
                "contact_person": item.contact_person,
                "email": item.email,
                "organization": item.organization,
                "application": item.application,
                "administration": item.administration,
            }

            token_instance = TokenAuth(**model_kwargs)

            try:
                token_instance.full_clean(exclude=("id",), validate_unique=False)
            except ValidationError as exception:
                exception_message = (
                    f"Validation error(s) occured for {item.identifier}."
                )
                raise ConfigurationRunFailed(exception_message) from exception

            logger.debug(f"No validation errors found for {item.identifier}")

            try:
                logger.debug(f"Saving {item.identifier}")

                TokenAuth.objects.update_or_create(
                    identifier=item.identifier,
                    defaults={
                        key: value
                        for key, value in model_kwargs.items()
                        if key != "identifier"
                    },
                )
            except IntegrityError as exception:
                exception_message = f"Failed configuring token {item.identifier}."
                raise ConfigurationRunFailed(exception_message) from exception

            logger.info(f"Configured {item.identifier}")


class SiteConfigurationStep(BaseConfigurationStep[TokenAuthGroupConfigurationModel]):
    """
    Configure configuration groups for the Objects API backend

    Configure the application site/domain.

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

    """
