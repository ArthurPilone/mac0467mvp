from django.db import models

from ..wppbot.models import ChatbotUser

class PartnerPromotion(models.Model):
    promotion_text = models.CharField(max_length=500)

class SingleUsePromotionalCode(models.Model):
    code = models.CharField(max_length=50)
    related_promotion = models.ForeignKey(PartnerPromotion, null=True, on_delete=models.SET_NULL)
    used = models.BooleanField(default=False)
    usedBy = models.ForeignKey(ChatbotUser, null=True, on_delete=models.SET_NULL)

class PartnerAdvert(models.Model):
    advert_text = models.CharField(max_length=500)