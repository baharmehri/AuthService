from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import CustomUserManager


# Create your models here.

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email
