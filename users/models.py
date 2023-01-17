from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser,BaseUserManager,AbstractBaseUser
from django.db import models
from django.utils import timezone
from users.managers import UserManager
from . import constants as user_constants


 
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email or not password:
            raise ValueError('User must have a username and password')

        user = self.model(
            email=CustomUserManager.normalize_email(email),
            **kwargs
        )

        user.set_password(password)
        user.save()

        return user
    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)

        user.is_admin = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):
    username = None # remove username field, we will use email as unique identifier
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=True, db_index=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    user_type = models.PositiveSmallIntegerField(choices=user_constants.USER_TYPE_CHOICES,null=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name="user_profile")
    phone = models.CharField(max_length=255,blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

