from apps.user.models import CustomUser
from apps.base.base_repository import BaseRepository


class UserRepository(BaseRepository):
    model = CustomUser

    @classmethod
    def check_user_exists(cls, number):
        user = cls.get_by_filter(number=number).first()
        return user

    @classmethod
    def insert_user_not_verified(cls, number):
        return cls.model.objects.create_user(number=number)
