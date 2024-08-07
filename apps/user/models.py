import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager


class CustomUser(AbstractUser):
    number = models.CharField(unique=True, max_length=11)
    username = models.CharField(max_length=255, null=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    banned_until = models.DateTimeField(null=True)

    USERNAME_FIELD = 'number'

    objects = CustomUserManager()
    REQUIRED_FIELDS = ('email',)

    def __str__(self):
        return self.number


class BannedIP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ip = models.CharField(max_length=255)
    banned_until = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(minutes=60))

    class Meta:
        unique_together = ('user', 'ip')
