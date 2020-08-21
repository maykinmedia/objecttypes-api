from rest_framework import viewsets

from objecttypes.core.models import ObjectType

from .serializers import ObjectTypeSerializer


class ObjectTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ObjectType.objects.prefetch_related("versions").order_by("-pk")
    serializer_class = ObjectTypeSerializer
    lookup_field = "uuid"
