from django.db import models
from django.utils.translation import ugettext_lazy as _

from solo.models import SingletonModel


class GithubConfig(SingletonModel):
    token = models.CharField(
        _("token"),
        max_length=250,
        blank=True,
        help_text=_(
            "Access token for GitHub authorization. Required for exporting. "
            "Can be generated at https://github.com/settings/tokens"
        ),
    )
    repo = models.CharField(
        _("repo"),
        max_length=250,
        help_text=_("GitHub repository in the format {owner}/{name}"),
    )
    folder = models.CharField(
        _("folder"),
        max_length=250,
        blank=True,
        help_text=_(
            "Path to the folder in the repository for import/export. "
            "If empty the root folder is used."
        ),
    )
    only_json = models.BooleanField(
        _("only JSON"),
        default=True,
        help_text=_("Show only .json files as import options"),
    )

    class Meta:
        verbose_name = _("GitHub configuration")
