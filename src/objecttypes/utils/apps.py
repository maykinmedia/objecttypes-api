from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = "objecttypes.utils"

    def ready(self):
        from . import oas_extensions  # noqa
