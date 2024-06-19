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
    "objecttypes.config",
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
    "objecttypes.config.site.SiteConfigurationStep",
    "objecttypes.config.objects.ObjectsAuthStep",
    "objecttypes.config.demo.DemoUserStep",
]


#
# Objecttypes settings
#

# setup_configuration command
# sites config
SITES_CONFIG_ENABLE = config("SITES_CONFIG_ENABLE", default=True, add_to_docs=False)
OBJECTTYPES_DOMAIN = config("OBJECTTYPES_DOMAIN", "", add_to_docs=False)
OBJECTTYPES_ORGANIZATION = config("OBJECTTYPES_ORGANIZATION", "", add_to_docs=False)
# objects auth config
OBJECTS_OBJECTTYPES_CONFIG_ENABLE = config(
    "OBJECTS_OBJECTTYPES_CONFIG_ENABLE", default=True, add_to_docs=False
)
OBJECTS_OBJECTTYPES_TOKEN = config("OBJECTS_OBJECTTYPES_TOKEN", "", add_to_docs=False)
OBJECTS_OBJECTTYPES_PERSON = config("OBJECTS_OBJECTTYPES_PERSON", "", add_to_docs=False)
OBJECTS_OBJECTTYPES_EMAIL = config("OBJECTS_OBJECTTYPES_EMAIL", "", add_to_docs=False)
# Demo User Configuration
DEMO_CONFIG_ENABLE = config("DEMO_CONFIG_ENABLE", default=DEBUG, add_to_docs=False)
DEMO_TOKEN = config("DEMO_TOKEN", "", add_to_docs=False)
DEMO_PERSON = config("DEMO_PERSON", "", add_to_docs=False)
DEMO_EMAIL = config("DEMO_EMAIL", "", add_to_docs=False)
