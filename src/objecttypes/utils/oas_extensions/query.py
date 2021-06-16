from drf_spectacular.contrib.django_filters import (
    DjangoFilterExtension as _DjangoFilterExtension,
)
from vng_api_common import filters


class DjangoFilterExtension(_DjangoFilterExtension):
    target_class = filters.Backend
    priority = 1
