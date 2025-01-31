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
    def create_user(self, email, password=None, **fields): 
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **fields)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, password=None, **fields):
        fields.setdefault('is_staff', True)
        fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **fields)



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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = []  

    def __str__(self): 
        return self.email 
    

