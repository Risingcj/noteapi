from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password,  user_type, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, user_type, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser has to have is staff being True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser has to have is superuser being True')

        return self.create_user(email=email, password=password, user_type=user_type, **extra_fields)


class CustomUser(AbstractUser):
    email = models.CharField(max_length=80, unique=True)
    username = models.CharField(max_length=45, unique=True)
    date_of_birth = models.DateField(null=True)
    user_type = models.CharField(max_length=10, choices=[('owner', 'Owner'), ('admin', 'Admin'), ('client', 'Client')])

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    def __str__(self):
        return self.username


class Owner(CustomUser):
    owner_field = models.CharField(max_length=50)


class Admin(CustomUser):
    admin_field = models.CharField(max_length=50)


class Client(CustomUser):
    client_field = models.CharField(max_length=50)
