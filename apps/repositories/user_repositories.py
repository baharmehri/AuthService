from apps.user.models import CustomUser


class UserRepository:
    @staticmethod
    def check_user_exists(number):
        return CustomUser.objects.filter(number=number).first()

    @staticmethod
    def insert_user_not_verified(number):
        return CustomUser.objects.create_user(number)
