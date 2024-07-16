import os
import sys
import warnings

os.environ.setdefault("DEBUG", "yes")
os.environ.setdefault("IS_HTTPS", "no")
os.environ.setdefault("ALLOWED_HOSTS", "*")
os.environ.setdefault(
    "SECRET_KEY", "fgv=c0hz&tl*8*3m3893@m+1pstrvidc9e^5@fpspmg%cy$15d"
)
os.environ.setdefault("ENVIRONMENT", "development")
os.environ.setdefault("RELEASE", "dev")

os.environ.setdefault("DB_NAME", "objecttypes"),
os.environ.setdefault("DB_USER", "objecttypes"),
os.environ.setdefault("DB_PASSWORD", "objecttypes"),

from .base import *  # noqa isort:skip

#
# Standard Django settings.
#

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGGING["loggers"].update(
    {
        "objecttypes": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["django"],
            "level": "DEBUG",
            "propagate": False,
        },
        "performance": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        #
        # See: https://code.djangoproject.com/ticket/30554
        # Autoreload logs excessively, turn it down a bit.
        #
        "django.utils.autoreload": {
            "handlers": ["django"],
            "level": "INFO",
            "propagate": False,
        },
    }
)

#
# Additional Django settings
#

# Disable security measures for development
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False

#
# Library settings
#

ELASTIC_APM["DEBUG"] = True

# Django debug toolbar
INSTALLED_APPS += [
    "debug_toolbar",
]
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
INTERNAL_IPS = ("127.0.0.1",)
DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}

AXES_BEHIND_REVERSE_PROXY = (
    False  # Default: False (we are typically using Nginx as reverse proxy)
)

# in memory cache and django-axes don't get along.
# https://django-axes.readthedocs.io/en/latest/configuration.html#known-configuration-problems
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },
    "axes_cache": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
    "oidc": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
}

AXES_CACHE = "axes_cache"


# THOU SHALT NOT USE NAIVE DATETIMES
warnings.filterwarnings(
    "error",
    r"DateTimeField .* received a naive datetime",
    RuntimeWarning,
    r"django\.db\.models\.fields",
)

# None of the authentication backends require two-factor authentication.
if config("DISABLE_2FA", default=True):  # pragma: no cover
    MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = AUTHENTICATION_BACKENDS

# Override settings with local settings.
try:
    from .local import *  # noqa
except ImportError:
    pass
