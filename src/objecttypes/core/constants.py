from django.utils.translation import ugettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices


class ObjectVersionStatus(DjangoChoices):
    published = ChoiceItem("published", _("Published"))
    draft = ChoiceItem("draft", _("Draft"))
    deprecated = ChoiceItem("deprecated", _("Deprecated"))


class DataClassificationChoices(DjangoChoices):
    open = ChoiceItem("open", _("Open"))
    intern = ChoiceItem("intern", _("Intern"))
    confidential = ChoiceItem("confidential", _("Confidential"))
    strictly_confidential = ChoiceItem(
        "strictly_confidential", _("Strictly confidential")
    )
