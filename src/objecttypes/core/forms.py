import json

from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from objecttypes.github.api import (
    create_file,
    get_files_in_folder,
    get_user,
    update_file,
)
from objecttypes.github.forms import GitHubFileField

from .models import ObjectType, ObjectVersion
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
        label=_("File"),
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


class ExportToGithubForm(forms.ModelForm):
    file_name = forms.CharField(
        label=_("File name"),
        max_length=100,
        required=True,
        help_text=_("Name ot the file in Github folder"),
    )
    overwrite = forms.BooleanField(
        label=_("Overwrite"),
        required=False,
        initial=False,
        help_text=_("Overwrite the existing file in the GitHub folder"),
    )
    github_folder_content = GitHubFileField(
        label=_("Folder content"),
        widget=forms.RadioSelect,
        disabled=True,
        required=False,
    )
    github_user = forms.CharField(
        label=_("User"),
        disabled=True,
        required=False,
        help_text=_("Github user. Can be configured in the Github Config page"),
    )

    class Meta:
        model = ObjectType
        fields = ("file_name", "overwrite", "github_folder_content", "github_user")

    def save(self, *args, **kwargs):
        json_schema = self.instance.last_version.json_schema
        json_str = json.dumps(json_schema)
        file_name = self.cleaned_data["file_name"]
        update = self.cleaned_data["update"]

        if update:
            return update_file(file_name, json_str)

        return create_file(file_name, json_str)

    def get_initial_for_field(self, field, field_name):
        if field_name == "github_user":
            user = get_user()
            return user.name

        return super().get_initial_for_field(field, field_name)

    def clean_file_name(self):
        file_name = self.cleaned_data["file_name"]
        overwrite = bool(self.data.get("overwrite", "").lower() == "on")

        self.cleaned_data["update"] = False
        existing_file_names = [file.name for file in get_files_in_folder()]

        if file_name in existing_file_names:
            self.cleaned_data["update"] = True

            if not overwrite:
                raise ValidationError(
                    "File with this name already exists. "
                    "Check 'overwrite' if you want to update the existing file "
                )
        return file_name
