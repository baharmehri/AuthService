from apps.user.models import CustomUser
from apps.base.repositories import BaseRepository


class UserRepository(BaseRepository):
    model = CustomUser

    @classmethod
    def check_user_exists(cls, number):
        account = cls.get_by_filter(number=number).first()
        return account

    @classmethod
    def insert_user_not_verified(cls, number):
        return cls.model.objects.create_user(number=number)

    @classmethod
    def verify_number(cls, number):
        account = cls.get_by_filter(number=number).first()
        if account is None:
            return None
        return cls.update(account, is_verified=True)
