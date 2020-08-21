import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .constants import ObjectTypeStatus


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
    public = models.BooleanField(
        _("public"),
        default=True,
        help_text="Indicates whether this data is accessible without any specific authorizations",
    )
    maintainer = models.CharField(
        _("maintainer"),
        max_length=200,
        blank=True,
        help_text="Organization which is responsible for the object type",
    )
    contact = models.CharField(
        _("contact"),
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
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=ObjectTypeStatus.choices,
        default=ObjectTypeStatus.draft,
        help_text="Status of the object type",
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

    class Meta:
        unique_together = ("object_type", "version")

    def __str__(self):
        return f"{self.object_type} v.{self.version}"
