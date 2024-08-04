from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, number, is_active=True, is_admin=False, is_verified=False, **kwargs):
        if not number:
            raise ValueError("Users must have an number")

        user = self.model(is_active=is_active, number=number, is_admin=is_admin, is_verified=is_verified, **kwargs)
        user.save()
        return user

    def create_superuser(self, number, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_admin', True)
        kwargs.setdefault('is_verified', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if kwargs.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        if kwargs.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if kwargs.get('is_verified') is not True:
            raise ValueError('Superuser must have is_verified=True.')
        return self.create_user(number, password, **kwargs)
