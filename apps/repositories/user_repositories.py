import datetime

from apps.user.models import CustomUser, BannedIP
from apps.base.repositories import BaseRepository


class UserRepository(BaseRepository):
    model = CustomUser

    @classmethod
    def check_user_exists(cls, number):
        user = cls.get_by_filter(number=number).first()
        return user

    @classmethod
    def insert_user_not_verified(cls, number):
        return cls.model.objects.create_user(number=number)

    @classmethod
    def verify_number(cls, number):
        user = cls.get_by_filter(number=number).first()
        if user is None:
            return None
        return cls.update(user, is_verified=True)

    @classmethod
    def set_password(cls, user_id, password):
        user = cls.get_by_filter(id=user_id).set_password(password)
        user.save()
        return

    @classmethod
    def ban_user(cls, user: CustomUser, ban_minute: int):
        banned_until = datetime.datetime.utcnow() + datetime.timedelta(minutes=ban_minute)
        user = cls.update(user, banned_until=banned_until)
        user.save()
        return


class BannedIPRepository(BaseRepository):
    model = BannedIP


