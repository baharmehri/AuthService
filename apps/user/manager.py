from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, number, password, is_active=True, is_admin=False, **kwargs):
        if not number:
            raise ValueError("Users must have an number")
        if not password:
            raise ValueError("Users must have an password")

        user = self.model(is_active=is_active, number=number, is_admin=is_admin, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_admin', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if kwargs.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        if kwargs.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        return self.create_user(email, password, **kwargs)
