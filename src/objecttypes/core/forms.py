from django import forms
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from objecttypes.github.forms import GitHubFileField

from .models import ObjectVersion
from .utils import download_json_schema, import_json_schema


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
        self.cleaned_data["json"] = download_json_schema(url)

    @transaction.atomic()
    def save(self):
        form_json = self.cleaned_data.get("json")
        name_plural = self.data.get("name_plural").title()

        return import_json_schema(json_schema=form_json, name_plural=name_plural)


class GithubImportForm(forms.Form):
    file_path = GitHubFileField(
        label=_("GitHub file"),
        widget=forms.RadioSelect,
    )
    name_plural = forms.CharField(
        label=_("Plural name"),
        max_length=100,
        required=True,
        help_text=_("The plural name variant of the objecttype."),
    )

    def clean_file_path(self):
        url = self.cleaned_data["file_path"]
        self.cleaned_data["json"] = download_json_schema(url)

    @transaction.atomic()
    def save(self):
        form_json = self.cleaned_data.get("json")
        name_plural = self.data.get("name_plural").title()

        return import_json_schema(json_schema=form_json, name_plural=name_plural)


class ObjectVersionForm(forms.ModelForm):
    class Meta:
        model = ObjectVersion
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pass the initial value to the widget, this value is used in case
        # the new value is invalid JSON which causes the widget to break
        if "json_schema" in self.initial:
            self.fields["json_schema"].widget.initial = self.initial["json_schema"]
