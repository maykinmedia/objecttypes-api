from django_filters import filters
from vng_api_common.filtersets import FilterSet
from vng_api_common.utils import get_help_text

from objecttypes.core.models import ObjectType


class ObjectTypeFilterSet(FilterSet):
    publicData = filters.BooleanFilter(
        field_name="public_data",
        help_text=get_help_text("core.ObjectType", "public_data"),
    )

    class Meta:
        model = ObjectType
        fields = ("publicData",)
