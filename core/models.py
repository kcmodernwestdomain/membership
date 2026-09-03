from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

class Membership(models.Model):
    name = models.CharField(max_length=100)
    regular_plan = models.ForeignKey(Plan, related_name='regular_membership', on_delete=models.CASCADE, default='1000')
    vip_plan = models.ForeignKey(Plan, related_name='vip_membership', on_delete=models.CASCADE, default='1500')


class CreditCardInfo(models.Model):
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=10)
    cvv = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    name_on_card = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.card_number