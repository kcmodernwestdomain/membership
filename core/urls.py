from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views 
from .views import  MembershipListView

urlpatterns = [
    path('homepage/', views.homepage, name='posts_home'),
    path('memberships/', MembershipListView.as_view(), name='membership-list'),
    path('creditcards/', views.CreditCardInfoCreateView.as_view(), name='creditcard-list'),
    ]
