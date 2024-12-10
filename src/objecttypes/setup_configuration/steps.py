import logging

from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from django_setup_configuration.configuration import BaseConfigurationStep
from django_setup_configuration.exceptions import ConfigurationRunFailed

from objecttypes.setup_configuration.models import (
    SiteGroupConfigurationModel,
    TokenAuthGroupConfigurationModel,
)
from objecttypes.token.models import TokenAuth

logger = logging.getLogger(__name__)


class TokenAuthConfigurationStep(
    BaseConfigurationStep[TokenAuthGroupConfigurationModel]
):
    """
    Configure tokens for other applications to access Objecttypes API
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


class SitesConfigurationStep(BaseConfigurationStep[SiteGroupConfigurationModel]):
    """
    Configure the application site/domain.
    """

    namespace = "objecttypes_sites"
    enable_setting = "objecttypes_site_config_enable"

    verbose_name = "Configuration to set up Sites for ObjectTypes"
    config_model = SiteGroupConfigurationModel

    def execute(self, model: SiteGroupConfigurationModel) -> None:
        for item in model.items:
            logger.info(f"Configuring {item.domain}")

            model_kwargs = {
                "domain": item.domain,
                "name": item.name,
            }

            instance = Site(**model_kwargs)

            try:
                instance.full_clean(exclude=("id",), validate_unique=False)
            except ValidationError as exception:
                exception_message = f"Validation error(s) occured for {item.domain}."
                raise ConfigurationRunFailed(exception_message) from exception

            logger.debug(f"No validation errors found for {item.domain}")

            try:
                logger.debug(f"Saving {item.domain}")
                Site.objects.update_or_create(
                    domain=item.domain,
                    defaults={
                        key: value
                        for key, value in model_kwargs.items()
                        if key != "domain"
                    },
                )

            except IntegrityError as exception:
                exception_message = f"Failed configuring token {item.domain}."
                raise ConfigurationRunFailed(exception_message) from exception

            logger.info(f"Configured {item.domain}")
