from django.utils.translation import gettext_lazy as _
from django.db import models

class ChatbotUser(models.Model):
    user_contact_addr = models.CharField(max_length=40)
    number_of_reports = models.IntegerField(default=0)
    midReport = models.BooleanField(default=False)

class Report(models.Model):
    class ReportState(models.TextChoices):
        AWAIT_CATEGORY = "AWCT", _("Awaiting Category")
        AWAIT_DESCRIPTION = "AWDC", _("Awaiting Description")
        CONFIRM_DESCRIPTION = "CFDC", _("Awaiting Description")
        AWAIT_LOCATION = "AWLC", _("Awaiting Localization")
        DONE = "DONE", _("Done")

    report_state = models.CharField(
        max_length=4,
        choices=ReportState.choices,
        default=ReportState.AWAIT_CATEGORY,
    )

    author = models.ForeignKey(ChatbotUser, null=True, on_delete=models.SET_NULL)
    categoria = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    dateCreated = models.DateTimeField(auto_now_add=True)
    #localização