from .models import CustomUser


def update_user_info(user: CustomUser, username=None, first_name=None, last_name=None):
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if username is not None:
        user.username = username

    user.save()
    return user


def active_user(user: CustomUser):
    user.is_active = True
    user.save()
    return user
