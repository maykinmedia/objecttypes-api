from open_api_framework.conf.base import *  # noqa

from .api import *  # noqa

#
# Core Django settings
#

DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql"
DATABASES["default"]["CONN_MAX_AGE"] = config(
    "DB_CONN_MAX_AGE",
    default=0,
    # The default is set to `60` in the docker settings, so that's what is mentioned
    # in the help text as well
    help_text=(
        "The lifetime of a database connection, as an integer of seconds. "
        "Use 0 to close database connections at the end of each request — Django’s historical behavior. "
        "This setting must be set to 0 if connection pooling is used. Defaults to: ``60``."
    ),
    group="Database",
    auto_display_default=False,
    cast=lambda x: int(x) if x != "None" else None,
)

# https://docs.djangoproject.com/en/5.2/ref/databases/#connection-pool
# https://www.psycopg.org/psycopg3/docs/api/pool.html#the-connectionpool-class

DB_POOL_ENABLED = config(
    "DB_POOL_ENABLED",
    default=False,
    help_text=(
        "Whether to use connection pooling "
        "(requires ``DB_CONN_MAX_AGE`` to be set to 0)."
    ),
    group="Database",
)

DB_POOL_MIN_SIZE = config(
    "DB_POOL_MIN_SIZE",
    default=4,
    help_text=(
        "The minimum number of connection the pool will hold. "
        "The pool will actively try to create new connections if some are lost (closed, broken) "
        "and will try to never go below min_size."
    ),
    group="Database",
)

DB_POOL_MAX_SIZE = config(
    "DB_POOL_MAX_SIZE",
    default=None,
    help_text=(
        "The maximum number of connections the pool will hold. "
        "If None, or equal to min_size, the pool will not grow or shrink. "
        "If larger than min_size, the pool can grow if more than min_size connections "
        "are requested at the same time and will shrink back after the extra connections "
        "have been unused for more than max_idle seconds."
    ),
    group="Database",
)

DB_POOL_TIMEOUT = config(
    "DB_POOL_TIMEOUT",
    default=30,
    help_text=(
        "The default maximum time in seconds that a client can wait "
        "to receive a connection from the pool (using connection() or getconn()). "
        "Note that these methods allow to override the timeout default."
    ),
    group="Database",
)

DB_POOL_MAX_WAITING = config(
    "DB_POOL_MAX_WAITING",
    default=0,
    help_text=(
        "Maximum number of requests that can be queued to the pool, "
        "after which new requests will fail, raising TooManyRequests. 0 means no queue limit."
    ),
    group="Database",
)

DB_POOL_MAX_LIFETIME = config(
    "DB_POOL_MAX_LIFETIME",
    default=60 * 60,
    help_text=(
        "The maximum lifetime of a connection in the pool, in seconds. "
        "Connections used for longer get closed and replaced by a new one. "
        "The amount is reduced by a random 10% to avoid mass eviction"
    ),
    group="Database",
)

DB_POOL_MAX_IDLE = config(
    "DB_POOL_MAX_IDLE",
    default=10 * 60,
    help_text=(
        "Maximum time, in seconds, that a connection can stay unused in the pool "
        "before being closed, and the pool shrunk. This only happens to "
        "connections more than min_size, if max_size allowed the pool to grow."
    ),
    group="Database",
)

DB_POOL_RECONNECT_TIMEOUT = config(
    "DB_POOL_RECONNECT_TIMEOUT",
    default=5 * 60,
    help_text=(
        "Maximum time, in seconds, the pool will try to create a connection. "
        "If a connection attempt fails, the pool will try to reconnect a few times, "
        "using an exponential backoff and some random factor to avoid mass attempts. "
        "If repeated attempts fail, after reconnect_timeout second the connection "
        "attempt is aborted and the reconnect_failed() callback invoked."
    ),
    group="Database",
)

DB_POOL_NUM_WORKERS = config(
    "DB_POOL_NUM_WORKERS",
    default=3,
    help_text=(
        "Number of background worker threads used to maintain the pool state. "
        "Background workers are used for example to create new connections and "
        "to clean up connections when they are returned to the pool."
    ),
    group="Database",
)


if DB_POOL_ENABLED:
    # FIXME Workaround for https://github.com/elastic/apm-agent-python/issues/2094
    # apm-agent-python does not instrument ConnectionPool yet
    import psycopg

    class WrapperConnectionClass(psycopg.Connection):
        @classmethod
        def connect(
            cls,
            conninfo: str = "",
            **kwargs,
        ) -> "psycopg.Connection[psycopg.rows.TupleRow]":
            return psycopg.connect(conninfo, **kwargs)

    DATABASES["default"]["OPTIONS"] = {
        "pool": {
            "min_size": DB_POOL_MIN_SIZE,
            "max_size": DB_POOL_MAX_SIZE,
            "timeout": DB_POOL_TIMEOUT,
            "max_waiting": DB_POOL_MAX_WAITING,
            "max_lifetime": DB_POOL_MAX_LIFETIME,
            "max_idle": DB_POOL_MAX_IDLE,
            "reconnect_timeout": DB_POOL_RECONNECT_TIMEOUT,
            "num_workers": DB_POOL_NUM_WORKERS,
            "connection_class": WrapperConnectionClass,
        }
    }

# Application definition
INSTALLED_APPS = INSTALLED_APPS + [
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
