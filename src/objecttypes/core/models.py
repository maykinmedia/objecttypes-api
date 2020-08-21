import uuid

from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from jsonschema.exceptions import SchemaError
from jsonschema.validators import validator_for

from .constants import ObjectVersionStatus


class ObjectType(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unique identifier (UUID4)"
    )
    name = models.CharField(
        _("name"), max_length=100, help_text="Name of the object type"
    )
    name_plural = models.CharField(
        _("name plural"), max_length=100, help_text="Plural name of the object type"
    )
    description = models.CharField(
        _("description"),
        max_length=1000,
        blank=True,
        help_text="The description of the object type",
    )
    public_data = models.BooleanField(
        _("public data"),
        default=True,
        help_text="Indicates whether this data is accessible without any specific authorizations",
    )
    maintainer_organization = models.CharField(
        _("maintainer organization"),
        max_length=200,
        blank=True,
        help_text="Organization which is responsible for the object type",
    )
    maintainer_contact_email = models.CharField(
        _("maintainer contact email"),
        max_length=200,
        blank=True,
        help_text="Person in the organization who can provide information about the object type",
    )
    domain = models.CharField(
        _("domain"),
        max_length=200,
        blank=True,
        help_text="Business department which is responsible for the object type",
    )

    def __str__(self):
        return f"{self.name}"


class ObjectVersion(models.Model):
    object_type = models.ForeignKey(
        ObjectType, on_delete=models.CASCADE, related_name="versions"
    )
    version = models.PositiveSmallIntegerField(
        _("version"), help_text=_("Integer version of the OBJECTTYPE")
    )
    publication_date = models.DateField(
        _("publication date"), auto_now=True, help_text=_("Date of Version publication")
    )
    json_schema = JSONField(
        _("JSON schema"), help_text="JSON schema for Object validation"
    )
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=ObjectVersionStatus.choices,
        default=ObjectVersionStatus.draft,
        help_text="Status of the object type version",
    )

    class Meta:
        unique_together = ("object_type", "version")

    def __str__(self):
        return f"{self.object_type} v.{self.version}"

    def clean(self):
        super().clean()

        schema_validator = validator_for(self.json_schema)
        try:
            schema_validator.check_schema(self.json_schema)
        except SchemaError as exc:
            raise ValidationError(exc.args[0]) from exc
