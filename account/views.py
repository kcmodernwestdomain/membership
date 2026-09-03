from django.contrib.auth import authenticate
from .serializers import SignUpSerializer, Logoutserializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .tokens import create_jwt_pair_for_user
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import ValidationError
from .serializers import ActivateUserByEmailSerializer
from django.contrib.auth import get_user_model
from .models import User
from rest_framework.exceptions import AuthenticationFailed



class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    @swagger_auto_schema(
        operation_summary='User Sign Up',
        operation_description='User Sign Up with this Endpoint'
    )
    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.create(serializer.validated_data)

                response = {
                    'message': 'User Successfully Created',
                    'data': {
                        'username': user.username,
                        'email': user.email,
                    }
                }

                return Response(data=response, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            error_message = e.detail.get('non_field_errors', [''])[0]
            return Response(data={'message': error_message}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_summary='JWT Login',
        operation_description='Login to get JWT tokens and user details',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, example="example@gmail.com"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, example="name"),
            },
            required=['email', 'password']
        )
    )
    def post(self, request: Request):
        email = request.data.get('email')
        password = request.data.get('password')

        print(f"Received login request - Email: {email}, Password: {password}")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            raise AuthenticationFailed("Account not Activated. Contact Admin to activate your account.")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)

            response = {
                'message': 'Login Successful',
                'tokens': tokens,
                'user': {
                    'fullname': getattr(user, 'fullname', ''),
                    'username': getattr(user, 'username', ''),
                    'email': getattr(user, 'email', ''),
                }
            }

            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request: Request):
        content = {
            'user': str(request.user),
            'auth': str(request.auth)
        }
        return Response(data=content, status=status.HTTP_200_OK)
    

class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Logoutserializer

    @swagger_auto_schema(
        operation_summary='Logout',
        operation_description='Logout User with this Endpoint'
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Logout successful'})


class FullNameView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({'fullname': user.full_name})
    
class AdminActivateUserView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'email',
                openapi.IN_QUERY,
                description="The email address of the user to activate",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: 'User activated successfully',
            400: 'Email query parameter is required',
            404: 'User with this email does not exist'
        }
    )
    def post(self, request):
        email = request.query_params.get('email')

        if not email:
            return Response({'message': 'Email query parameter is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User with this email does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)

        if user.is_active:
            return Response({'message': 'User account is already active.'},
                            status=status.HTTP_200_OK)

        user.is_active = True
        user.save()

        return Response({'message': f'User account {email} has been activated successfully.'},
                        status=status.HTTP_200_OK)
