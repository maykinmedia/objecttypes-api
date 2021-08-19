from json.decoder import JSONDecodeError

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import requests
from rest_framework import exceptions

from ..api.validators import JsonSchemaValidator


class UrlImportForm(forms.Form):
    objecttype_url = forms.URLField(
        label="Objecttype URL",
        widget=forms.TextInput(
            attrs={
                "placeholder": "https://example.com/boom.json",
                "size": 100,
            }
        ),
        required=True,
        help_text=_("The direct URL for a given objecttype file (JSON)."),
    )
    name_plural = forms.CharField(
        label=_("Plural name"),
        max_length=100,
        required=True,
        help_text=_("The plural name variant of the objecttype."),
    )

    def clean_objecttype_url(self):
        url = self.cleaned_data["objecttype_url"]

        try:
            response = requests.get(url)
        except requests.exceptions.RequestException:
            raise ValidationError("The Objecttype URL does not exist.")

        if response.status_code != requests.codes.ok:
            raise ValidationError("Objecttype URL returned non OK status.")

        try:
            response_json = response.json()
        except JSONDecodeError:
            raise ValidationError("Could not parse JSON from Objecttype URL.")

        json_schema_validator = JsonSchemaValidator()

        try:
            json_schema_validator(response_json)
        except exceptions.ValidationError as e:
            raise ValidationError(
                f"Invalid JSON schema. {e.detail[0]}.", code=e.detail[0].code
            )

        self.cleaned_data["json"] = response_json