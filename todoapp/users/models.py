from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Add manager methods here to create user and super user
    """

    def create(self, email, password=None, first_name=None, last_name=None, **fields):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(
            email=self.normalize_email(email), 
            first_name=first_name, 
            last_name=last_name, 
            **fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, first_name=None, last_name=None, **fields):
        return self.create_user(
            email, password, first_name, last_name, is_staff=True, is_superuser=True, **fields
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Needed fields
    - password (already inherited from AbstractBaseUser; encrypt password before saving to database)
    - last_login (already inherited from AbstractBaseUser)
    - is_superuser
    - first_name (max_length=30)
    - email (should be unique)
    - is_staff
    - date_joined (default should be time of object creation)
    - last_name (max_length=150)
    """
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, verbose_name='First Name')
    last_name = models.CharField(max_length=150, verbose_name='Last Name')
    email = models.EmailField(unique=True, verbose_name='Email')
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        default=timezone.now, editable=False, verbose_name='Date Joined'
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
