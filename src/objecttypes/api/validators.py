from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from objecttypes.core.constants import ObjectVersionStatus
from objecttypes.core.utils import check_json_schema


class VersionUpdateValidator:
    message = _("Only draft versions can be changed")
    code = "non-draft-version-update"

    def set_context(self, serializer):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer, "instance", None)
        self.request = serializer.context["request"]

    def __call__(self, attrs):
        if not self.instance:
            return

        if self.instance.status != ObjectVersionStatus.draft:
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

    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.serializer_field = serializer_field
        self.instance = getattr(serializer_field.parent, "instance", None)

    def __call__(self, new_value):
        # no instance -> it's not an update
        if not self.instance:
            return

        current_value = getattr(self.instance, self.serializer_field.source)

        if new_value != current_value:
            raise serializers.ValidationError(self.message, code=self.code)
