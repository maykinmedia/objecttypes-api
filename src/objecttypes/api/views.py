from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from vng_api_common.viewsets import NestedViewSetMixin

from objecttypes.core.constants import ObjectVersionStatus
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

    @swagger_auto_schema(request_body=no_body)
    @action(detail=True, methods=["post"])
    def publish(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = ObjectVersionStatus.published
        instance.save()

        serializer = self.get_serializer(instance)

        return Response(serializer.data)
