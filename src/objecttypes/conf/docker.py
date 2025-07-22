import os

os.environ.setdefault("DB_HOST", "db")
os.environ.setdefault("DB_NAME", "postgres")
os.environ.setdefault("DB_USER", "postgres")
os.environ.setdefault("DB_PASSWORD", "")
os.environ.setdefault("DB_CONN_MAX_AGE", "60")

os.environ.setdefault("ENVIRONMENT", "docker")
os.environ.setdefault("LOG_STDOUT", "yes")
os.environ.setdefault("LOG_FORMAT_CONSOLE", "json")

from .production import *  # noqa isort:skip
