from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager


# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email
