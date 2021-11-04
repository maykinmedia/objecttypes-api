from email.utils import parsedate_to_datetime
from typing import List, Tuple

from django import forms

from .api import get_files_in_folder, get_last_commit_for_file


def get_import_choices() -> List[Tuple[str, str]]:
    choices = []
    files = get_files_in_folder()
    for file in files:
        last_commit = get_last_commit_for_file(file.path)
        last_date = parsedate_to_datetime(last_commit.last_modified).date()
        description = f"{file.name} ({last_date}) by {last_commit.author.name}"
        choices.append((file.download_url, description))

    return choices


class GitHubFileField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs["choices"] = get_import_choices

        super().__init__(*args, **kwargs)
