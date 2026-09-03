# memberships/serializers.py
from rest_framework import serializers
from .models import Plan, Membership
from .models import CreditCardInfo

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price']

class MembershipSerializer(serializers.ModelSerializer):
    regular_plan = PlanSerializer()
    vip_plan = PlanSerializer()

    class Meta:
        model = Membership
        fields = [ 'regular_plan', 'vip_plan']




class CreditCardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCardInfo
        fields = '__all__'



