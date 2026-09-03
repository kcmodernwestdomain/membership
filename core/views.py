# memberships/views.py
from django.http import HttpRequest,JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, authenticate
from .models import Membership
from rest_framework.response import Response
from .serializers import MembershipSerializer
from .models import CreditCardInfo
from .serializers import CreditCardInfoSerializer


def homepage(requeest:HttpRequest):
    respose={'message':'Hello World'}
    return JsonResponse(data=respose)


class MembershipListView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer





class CreditCardInfoCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreditCardInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)