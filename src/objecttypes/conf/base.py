from pathlib import Path

import structlog
from open_api_framework.conf.base import *  # noqa

from .api import *  # noqa

#
# Core Django settings
#


# Application definition
INSTALLED_APPS = INSTALLED_APPS + [
    # External applications.
    "jsonsuit.apps.JSONSuitConfig",
    "django_structlog",
    # Two-factor authentication in the Django admin, enforced.
    # Project applications.
    "objecttypes.accounts",
    "objecttypes.api",
    "objecttypes.setup_configuration",
    "objecttypes.core",
    "objecttypes.token",
    "objecttypes.utils",
]

#
# LOGGING
#

# XXX: this should be renamed to `LOG_REQUESTS` in the next major release
_log_requests_via_middleware = config(
    "ENABLE_STRUCTLOG_REQUESTS",
    default=True,
    help_text=("enable structured logging of requests"),
    group="Logging",
)
if _log_requests_via_middleware:
    MIDDLEWARE.insert(
        MIDDLEWARE.index("django.contrib.auth.middleware.AuthenticationMiddleware") + 1,
        "django_structlog.middlewares.RequestMiddleware",
    )

# TODO move this back to OAF
# Override LOGGING, because OAF does not yet apply structlog for all components
logging_root_handlers = ["console"] if LOG_STDOUT else ["json_file"]
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        # structlog - foreign_pre_chain handles logs coming from stdlib logging module,
        # while the `structlog.configure` call handles everything coming from structlog.
        # They are mutually exclusive.
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": [
                structlog.contextvars.merge_contextvars,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
            ],
        },
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
            "foreign_pre_chain": [
                structlog.contextvars.merge_contextvars,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
            ],
        },
        "verbose": {
            "format": "%(asctime)s %(levelname)s %(name)s %(module)s %(process)d %(thread)d  %(message)s"
        },
        "timestamped": {"format": "%(asctime)s %(levelname)s %(name)s  %(message)s"},
        "simple": {"format": "%(levelname)s  %(message)s"},
        "performance": {"format": "%(asctime)s %(process)d | %(thread)d | %(message)s"},
        "db": {"format": "%(asctime)s | %(message)s"},
        "outgoing_requests": {"()": HttpFormatter},
    },
    # TODO can be removed?
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
    },
    "handlers": {
        # TODO can be removed?
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": config(
                "LOG_FORMAT_CONSOLE",
                default="json",
                help_text=(
                    "The format for the console logging handler, possible options: ``json``, ``plain_console``."
                ),
                group="Logging",
            ),
        },
        "console_db": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "db",
        },
        # replaces the "django" and "project" handlers - in containerized applications
        # the best practices is to log to stdout (use the console handler).
        "json_file": {
            "level": LOG_LEVEL,  # always debug might be better?
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGGING_DIR) / "application.jsonl",
            "formatter": "json",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "performance": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGGING_DIR) / "performance.log",
            "formatter": "performance",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "requests": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGGING_DIR) / "requests.log",
            "formatter": "timestamped",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "log_outgoing_requests": {
            "level": "DEBUG",
            "formatter": "outgoing_requests",
            "class": "logging.StreamHandler",  # to write to stdout
        },
        "save_outgoing_requests": {
            "level": "DEBUG",
            # enabling saving to database
            "class": "log_outgoing_requests.handlers.DatabaseOutgoingRequestsHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": logging_root_handlers,
            "level": "ERROR",
            "propagate": False,
        },
        PROJECT_DIRNAME: {
            "handlers": logging_root_handlers,
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "mozilla_django_oidc": {
            "handlers": logging_root_handlers,
            "level": LOG_LEVEL,
        },
        f"{PROJECT_DIRNAME}.utils.middleware": {
            "handlers": logging_root_handlers,
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "vng_api_common": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["console_db"] if LOG_QUERIES else [],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.request": {
            "handlers": logging_root_handlers,
            "level": LOG_LEVEL,
            "propagate": False,
        },
        # suppress django.server request logs because those are already emitted by
        # django-structlog middleware
        "django.server": {
            "handlers": ["console"],
            "level": "WARNING" if _log_requests_via_middleware else "INFO",
            "propagate": False,
        },
        "django.template": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "log_outgoing_requests": {
            "handlers": (
                ["log_outgoing_requests", "save_outgoing_requests"]
                if LOG_REQUESTS
                else []
            ),
            "level": "DEBUG",
            "propagate": True,
        },
        "django_structlog": {
            "handlers": logging_root_handlers,
            "level": "INFO",
            "propagate": False,
        },
    },
}

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        # structlog.processors.ExceptionPrettyPrinter(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

#
# DJANGO-STRUCTLOG
#
DJANGO_STRUCTLOG_IP_LOGGING_ENABLED = False

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
    "objecttypes.setup_configuration.steps.token_auth.TokenAuthConfigurationStep",
    "mozilla_django_oidc_db.setup_configuration.steps.AdminOIDCConfigurationStep",
]
