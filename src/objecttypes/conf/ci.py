"""
Continuous integration settings module.
"""

import logging
import os

os.environ.setdefault("SECRET_KEY", "dummy")
os.environ.setdefault("ENVIRONMENT", "ci")
os.environ.setdefault("IS_HTTPS", "no")

from .base import *  # noqa isort:skip

CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
    # https://github.com/jazzband/django-axes/blob/master/docs/configuration.rst#cache-problems
    "axes": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
    "oas": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
    "sessions": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
    "oidc": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
}

LOGGING = None  # Quiet is nice
logging.disable(logging.CRITICAL)

#
# Django-axes
#
AXES_BEHIND_REVERSE_PROXY = False
