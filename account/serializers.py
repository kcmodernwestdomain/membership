from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User
from rest_framework.authtoken.models import Token



class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, write_only=True)
    phone_number = serializers.CharField(max_length=17)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'username', 'password', 'phone_number']

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()
        username_exists = User.objects.filter(username=attrs['username']).exists()
        phone_number_exists = User.objects.filter(phone_number=attrs['phone_number']).exists()

        if email_exists:
            raise serializers.ValidationError('The Email has already been used')

        if username_exists:
            raise serializers.ValidationError('The Username has already been used')

        if phone_number_exists:
            raise serializers.ValidationError('The Phone Number has already been used')

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class Logoutserializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):

        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise ValidationError('bad_token')


class ActivateUserByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()