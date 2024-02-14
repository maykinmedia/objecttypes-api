from django.utils.translation import gettext_lazy as _

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


class UpdateFrequencyChoices(DjangoChoices):
    real_time = ChoiceItem("real_time", _("Real-time"))
    hourly = ChoiceItem("hourly", _("Hourly"))
    daily = ChoiceItem("daily", _("Daily"))
    weekly = ChoiceItem("weekly", _("Weekly"))
    monthly = ChoiceItem("monthly", _("Monthly"))
    yearly = ChoiceItem("yearly", _("Yearly"))
    unknown = ChoiceItem("unknown", _("Unknown"))
