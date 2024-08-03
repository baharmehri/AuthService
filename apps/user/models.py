from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager


# Create your models here.

class CustomUser(AbstractUser):
    number = models.IntegerField(unique=True, max_length=11)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'number'

    objects = CustomUserManager()
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.number
