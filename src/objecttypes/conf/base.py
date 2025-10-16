import os

os.environ["_USE_STRUCTLOG"] = "True"

from open_api_framework.conf.base import *  # noqa

from .api import *  # noqa

#
# Core Django settings
#


# Application definition
INSTALLED_APPS = INSTALLED_APPS + [
    "maykin_common",
    "capture_tag",
    # External applications.
    "jsonsuit.apps.JSONSuitConfig",
    # Two-factor authentication in the Django admin, enforced.
    # Project applications.
    "objecttypes.accounts",
    "objecttypes.api",
    "objecttypes.setup_configuration",
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

# Default (connection timeout, read timeout) for the requests library (in seconds)
REQUESTS_DEFAULT_TIMEOUT = (10, 30)

##############################
#                            #
# 3RD PARTY LIBRARY SETTINGS #
#                            #
##############################

# Django-Admin-Index
ADMIN_INDEX_DISPLAY_DROP_DOWN_MENU_CONDITION_FUNCTION = (
    "maykin_common.django_two_factor_auth.should_display_dropdown_menu"
)

#
# Django setup configuration
#
SETUP_CONFIGURATION_STEPS = [
    "objecttypes.setup_configuration.steps.token_auth.TokenAuthConfigurationStep",
    "mozilla_django_oidc_db.setup_configuration.steps.AdminOIDCConfigurationStep",
]

#
# SECURITY settings
#
CSRF_FAILURE_VIEW = "maykin_common.views.csrf_failure"

# This setting is used by the csrf_failure view (accounts app).
# You can specify any path that should match the request.path
# Note: the LOGIN_URL Django setting is not used because you could have
# multiple login urls defined.
LOGIN_URLS = [reverse_lazy("admin:login")]
