from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from objecttypes.core.constants import ObjectVersionStatus
from objecttypes.core.utils import check_json_schema


class VersionUpdateValidator:
    message = _("Only draft versions can be changed")
    code = "non-draft-version-update"
    requires_context = True

    def __call__(self, attrs, serializer):
        instance = getattr(serializer, "instance", None)
        if not instance:
            return

        if instance.status != ObjectVersionStatus.draft:
            raise serializers.ValidationError(self.message, code=self.code)


class JsonSchemaValidator:
    code = "invalid-json-schema"

    def __call__(self, value):
        try:
            check_json_schema(value)
        except ValidationError as exc:
            raise serializers.ValidationError(exc.args[0], code=self.code) from exc


class IsImmutableValidator:
    """
    Validate that the field should not be changed in update action
    """

    message = _("This field can't be changed")
    code = "immutable-field"
    requires_context = True

    def __call__(self, new_value, serializer_field):
        # no instance -> it's not an update
        instance = getattr(serializer_field.parent, "instance", None)
        if not instance:
            return

        current_value = getattr(instance, serializer_field.source)

        if new_value != current_value:
            raise serializers.ValidationError(self.message, code=self.code)
