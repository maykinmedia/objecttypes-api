from django.utils.translation import ugettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices


class ObjectVersionStatus(DjangoChoices):
    published = ChoiceItem("published", _("Published"))
    draft = ChoiceItem("draft", _("Draft"))
    deprecated = ChoiceItem("deprecated", _("Deprecated"))
