from django import forms


class UrlImportForm(forms.Form):
    github_url = forms.URLField(
        label="GitHub URL",
        widget=forms.TextInput(
            attrs={
                "placeholder": "https://example.com/boom.json",
                "size": 100,
            }
        ),
    )
    name_plural = forms.CharField(max_length=100)
