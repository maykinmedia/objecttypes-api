from open_api_framework.conf.base import *  # noqa
from open_api_framework.conf.utils import config

from .api import *  # noqa

init_sentry()

#
# Core Django settings
#

# Application definition
INSTALLED_APPS = INSTALLED_APPS + [
    # External applications.
    "jsonsuit.apps.JSONSuitConfig",
    # Two-factor authentication in the Django admin, enforced.
    "sharing_configs",
    # Project applications.
    "objecttypes.accounts",
    "objecttypes.api",
    "objecttypes.core",
    "objecttypes.token",
    "objecttypes.utils",
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"  # FIXME should this be "nl-nl"?

TIME_ZONE = "Europe/Amsterdam"  # FIXME should this be "UTC"?

#
# Custom settings
#
PROJECT_NAME = "Objecttypes"
SITE_TITLE = "Starting point"


##############################
#                            #
# 3RD PARTY LIBRARY SETTINGS #
#                            #
##############################

# Django-Admin-Index
ADMIN_INDEX_DISPLAY_DROP_DOWN_MENU_CONDITION_FUNCTION = (
    "objecttypes.utils.admin_index.should_display_dropdown_menu"
)

#
# Django setup configuration
#
SETUP_CONFIGURATION_STEPS = [
    "objecttypes.setup_configuration.steps.SitesConfigurationStep",
    "objecttypes.setup_configuration.steps.TokenAuthConfigurationStep",
]
