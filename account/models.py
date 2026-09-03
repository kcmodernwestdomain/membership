from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        user.is_active = False  
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.CharField(max_length=80, unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField(null=True)
    phone_number = models.CharField(max_length=17, unique=True)
    address = models.CharField(max_length=70)
    Bio = models.CharField(max_length=70)
    fullname = models.CharField(max_length=70)


    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Add related_name to avoid conflicts
    groups = models.ManyToManyField('auth.Group', related_name='user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='user_permissions')

    def __str__(self):
        return self.username
