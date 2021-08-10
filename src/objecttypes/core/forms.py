from django import forms
from django.utils.translation import ugettext_lazy as _


class UrlImportForm(forms.Form):
    objecttype_url = forms.URLField(
        label="Objecttype URL",
        widget=forms.TextInput(
            attrs={
                "placeholder": "https://example.com/boom.json",
                "size": 100,
            }
        ),
    )
    name_plural = forms.CharField(
        label=_("Plural name"),
        max_length=100,
    )
