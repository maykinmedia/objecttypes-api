from django_filters import filters
from vng_api_common.filtersets import FilterSet
from vng_api_common.utils import get_help_text

from objecttypes.core.constants import DataClassificationChoices
from objecttypes.core.models import ObjectType


class ObjectTypeFilterSet(FilterSet):
    dataClassification = filters.ChoiceFilter(
        field_name="data_classification",
        choices=DataClassificationChoices.choices,
        help_text=get_help_text("core.ObjectType", "data_classification"),
    )

    class Meta:
        model = ObjectType
        fields = ("dataClassification",)
