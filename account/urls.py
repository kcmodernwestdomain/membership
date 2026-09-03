from . import views
from . views import  LogoutView, FullNameView, AdminActivateUserView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name="login"),
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwn_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get-fullname/', FullNameView.as_view(), name='get-fullname'),
    path('admin/activate-user/', AdminActivateUserView.as_view(), name='admin-activate-user')
]
