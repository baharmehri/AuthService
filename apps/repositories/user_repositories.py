from apps.user.models import CustomUser


class UserRepository:
    @staticmethod
    def check_user_exists(number):
        return CustomUser.objects.filter(phone_number=number).first()
