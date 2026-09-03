# yourapp/admin.py

from django.contrib import admin
from .models import Plan, Membership, CreditCardInfo

admin.site.register(Plan)
admin.site.register(Membership)
admin.site.register(CreditCardInfo)
