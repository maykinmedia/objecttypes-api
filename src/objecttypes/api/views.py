from rest_framework import mixins, viewsets
from vng_api_common.viewsets import NestedViewSetMixin

from objecttypes.core.models import ObjectType, ObjectVersion

from .filters import ObjectTypeFilterSet
from .serializers import ObjectTypeSerializer, ObjectVersionSerializer


class ObjectTypeViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet
):
    queryset = ObjectType.objects.prefetch_related("versions").order_by("-pk")
    serializer_class = ObjectTypeSerializer
    lookup_field = "uuid"
    filterset_class = ObjectTypeFilterSet


class ObjectVersionViewSet(
    NestedViewSetMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.ReadOnlyModelViewSet,
):
    queryset = ObjectVersion.objects.order_by("object_type", "-version")
    serializer_class = ObjectVersionSerializer
    lookup_field = "version"
