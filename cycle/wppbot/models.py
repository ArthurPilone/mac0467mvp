from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.
class ChatbotUser(models.Model):
    user_contact_addr = models.CharField(max_length=40)
    number_of_reports = models.IntegerField(default=0)
    midReport = models.BooleanField(default=False)

class Report(models.Model):
    class ReportState(models.TextChoices):
        OPEN = "OPEN", _("Open")
        AWAIT_CATEGORY = "AWCT", _("Awaiting Category")
        DONE = "DONE", _("Done")

    report_state = models.CharField(
        max_length=4,
        choices=ReportState.choices,
        default=ReportState.OPEN,
    )

    authorId = models.ForeignKey(ChatbotUser, null=True, on_delete=models.SET_NULL)
    categoria = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    #localização
    