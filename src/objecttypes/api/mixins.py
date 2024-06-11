from django.core.exceptions import ValidationError
from django.http import Http404

from rest_framework_nested.viewsets import NestedViewSetMixin as _NestedViewSetMixin


class NestedViewSetMixin(_NestedViewSetMixin):
    def get_queryset(self):
        """
        catch validation errors if parent_lookup_kwargs have incorrect format
        and return 404
        """
        try:
            queryset = super().get_queryset()
        except ValidationError:
            raise Http404

        return queryset
