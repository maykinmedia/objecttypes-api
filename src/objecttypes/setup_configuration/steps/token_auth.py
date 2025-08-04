from django.core.exceptions import ValidationError
from django.db import IntegrityError

import structlog
from django_setup_configuration.configuration import BaseConfigurationStep
from django_setup_configuration.exceptions import ConfigurationRunFailed

from objecttypes.setup_configuration.models.token_auth import (
    TokenAuthGroupConfigurationModel,
)
from objecttypes.token.models import TokenAuth

logger = structlog.stdlib.get_logger(__name__)


class TokenAuthConfigurationStep(
    BaseConfigurationStep[TokenAuthGroupConfigurationModel]
):
    """
    Configure tokens for other applications to access Objecttypes API
    """

    namespace = "tokenauth"
    enable_setting = "tokenauth_config_enable"

    verbose_name = "Configuration to set up authentication tokens for ObjectTypes"
    config_model = TokenAuthGroupConfigurationModel

    def execute(self, model: TokenAuthGroupConfigurationModel) -> None:
        if len(model.items) == 0:
            logger.warning("no_tokens_defined")

        for item in model.items:
            logger.info("configuring_token", token_identifier=item.identifier)

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

            try:
                logger.debug("save_token_to_database", token_identifier=item.identifier)

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

            logger.info("token_configuration_success", token_identifier=item.identifier)
