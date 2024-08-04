from apps.repositories.base_repository import BaseRepository
from apps.user.models import User


class UserRepository(BaseRepository):

    def __init__(self, user: User):
        super().__init__(user)

    @staticmethod
    def check_user_exists(number):
        return User.objects.filter(number=number).first()

    @staticmethod
    def insert_user_not_verified(number):
        return User.objects.create_user(number)
