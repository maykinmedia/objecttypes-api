import logging

from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from django_setup_configuration.configuration import BaseConfigurationStep
from django_setup_configuration.exceptions import ConfigurationRunFailed

from objecttypes.setup_configuration.models.sites import SitesConfigurationModel

logger = logging.getLogger(__name__)


class SitesConfigurationStep(BaseConfigurationStep[SitesConfigurationModel]):
    """
    Configure the application site/domain.
    """

    namespace = "objecttypes_sites"
    enable_setting = "objecttypes_sites_config_enable"

    verbose_name = "Configuration to set up Sites for ObjectTypes"
    config_model = SitesConfigurationModel

    def execute(self, model: SitesConfigurationModel) -> None:
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
