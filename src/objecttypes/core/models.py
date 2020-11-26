import uuid
from datetime import date

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .constants import (
    DataClassificationChoices,
    ObjectVersionStatus,
    UpdateFrequencyChoices,
)
from .utils import check_json_schema


class ObjectType(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text=_("Unique identifier (UUID4)")
    )
    name = models.CharField(
        _("name"), max_length=100, help_text=_("Name of the object type")
    )
    name_plural = models.CharField(
        _("name plural"), max_length=100, help_text=_("Plural name of the object type")
    )
    description = models.CharField(
        _("description"),
        max_length=1000,
        blank=True,
        help_text=_("The description of the object type"),
    )
    data_classification = models.CharField(
        _("data classification"),
        max_length=20,
        choices=DataClassificationChoices.choices,
        default=DataClassificationChoices.open,
        help_text=_("Confidential level of the object type"),
    )
    maintainer_organization = models.CharField(
        _("maintainer organization"),
        max_length=200,
        blank=True,
        help_text=_("Organization which is responsible for the object type"),
    )
    maintainer_department = models.CharField(
        _("maintainer department"),
        max_length=200,
        blank=True,
        help_text=_("Business department which is responsible for the object type"),
    )
    contact_person = models.CharField(
        _("contact person"),
        max_length=200,
        blank=True,
        help_text=_(
            "Name of the person in the organization who can provide information about the object type"
        ),
    )
    contact_email = models.CharField(
        _("contact email"),
        max_length=200,
        blank=True,
        help_text=_(
            "Email of the person in the organization who can provide information about the object type"
        ),
    )
    source = models.CharField(
        _("source"),
        max_length=200,
        blank=True,
        help_text=_("Name of the system from which the object type originates"),
    )
    update_frequency = models.CharField(
        _("update frequency"),
        max_length=10,
        choices=UpdateFrequencyChoices.choices,
        default=UpdateFrequencyChoices.unknown,
        help_text=_("Indicates how often the object type is updated"),
    )
    provider_organization = models.CharField(
        _("provider organization"),
        max_length=200,
        blank=True,
        help_text=_(
            "Organization which is responsible for publication of the object type"
        ),
    )
    documentation_url = models.URLField(
        _("documentation url"),
        blank=True,
        help_text=_("Link to the documentation for the object type"),
    )
    labels = JSONField(
        _("labels"),
        help_text=_("Key-value pairs of keywords related for the object type"),
        default=dict,
        blank=True,
    )
    created_at = models.DateField(
        _("created at"),
        auto_now_add=True,
        help_text=_("Date when the object type was created"),
    )
    modified_at = models.DateField(
        _("modified at"),
        auto_now=True,
        help_text=_("Last date when the object type was modified"),
    )

    def __str__(self):
        return f"{self.name}"

    @property
    def last_version(self):
        if not self.versions:
            return None

        return self.versions.order_by("-version").first()

    @property
    def ordered_versions(self):
        return self.versions.order_by("-version")


class ObjectVersion(models.Model):
    object_type = models.ForeignKey(
        ObjectType, on_delete=models.CASCADE, related_name="versions"
    )
    version = models.PositiveSmallIntegerField(
        _("version"), help_text=_("Integer version of the OBJECTTYPE")
    )
    created_at = models.DateField(
        _("created at"),
        auto_now_add=True,
        help_text=_("Date when the version was created"),
    )
    modified_at = models.DateField(
        _("modified at"),
        auto_now=True,
        help_text=_("Last date when the version was modified"),
    )
    published_at = models.DateField(
        _("published_at"), null=True, help_text=_("Date when the version was published")
    )
    json_schema = JSONField(
        _("JSON schema"), help_text=_("JSON schema for Object validation"), default=dict
    )
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=ObjectVersionStatus.choices,
        default=ObjectVersionStatus.draft,
        help_text=_("Status of the object type version"),
    )

    class Meta:
        unique_together = ("object_type", "version")

    def __str__(self):
        return f"{self.object_type} v.{self.version}"

    def clean(self):
        super().clean()

        check_json_schema(self.json_schema)

    def save(self, *args, **kwargs):
        if not self.version:
            self.version = self.generate_version_number()

        super().save(*args, **kwargs)

    def generate_version_number(self) -> int:
        existed_versions = ObjectVersion.objects.filter(object_type=self.object_type)

        max_version = 0
        if existed_versions.exists():
            max_version = existed_versions.aggregate(models.Max("version"))[
                "version__max"
            ]

        version_number = max_version + 1
        return version_number
