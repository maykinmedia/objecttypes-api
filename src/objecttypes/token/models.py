import secrets

from django.db import models
from django.utils.translation import gettext_lazy as _

from objecttypes.token.validators import validate_no_empty, validate_no_whitespace


class TokenAuth(models.Model):
    identifier = models.SlugField(
        unique=True,
        help_text=_("A human-friendly label to refer to this token"),
    )

    token = models.CharField(
        _("token"),
        max_length=40,
        unique=True,
        validators=[validate_no_empty, validate_no_whitespace],
    )

    contact_person = models.CharField(
        _("contact person"),
        max_length=200,
        help_text=_("Name of the person in the organization who can access the API"),
    )
    email = models.EmailField(
        _("email"),
        help_text=_("Email of the person, who can access the API"),
    )
    organization = models.CharField(
        _("organization"),
        max_length=200,
        blank=True,
        help_text=_("Organization which has access to the API"),
    )
    last_modified = models.DateTimeField(
        _("last modified"),
        auto_now=True,
        help_text=_("Last date when the token was modified"),
    )
    created = models.DateTimeField(
        _("created"),
        auto_now_add=True,
        help_text=_("Date when the token was created"),
    )
    application = models.CharField(
        _("application"),
        max_length=200,
        blank=True,
        help_text=_("Application which has access to the API"),
    )
    administration = models.CharField(
        _("administration"),
        max_length=200,
        blank=True,
        help_text=_("Administration which has access to the API"),
    )

    class Meta:
        verbose_name = _("token authorization")
        verbose_name_plural = _("token authorizations")

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        return super().save(*args, **kwargs)

    def generate_token(self):
        return secrets.token_hex(20)
