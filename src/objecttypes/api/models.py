import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


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

    def __str__(self):
        return f"{self.name}"


class ObjectVersion(models.Model):
    object_type = models.ForeignKey(
        ObjectType, on_delete=models.CASCADE, related_name="versions"
    )
    version = models.SmallIntegerField(
        _("version"), help_text=_("Integer version of the OBJECTTYPE")
    )
    publication_date = models.DateField(
        _("publication date"), auto_now=True, help_text=_("Date of Version publication")
    )
    json_schema = models.URLField(
        _("JSON schema"), help_text="Url reference to JSON schema for Object validation"
    )

    class Meta:
        unique_together = ("object_type", "version")

    def __str__(self):
        return f"{self.object_type} v.{self.version}"
