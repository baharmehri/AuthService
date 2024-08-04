import random
from django.contrib.auth import authenticate

from apps.utils.redis import get_redis_connection
from apps.repositories.user_repositories import UserRepository


class UserServices:
    def __init__(self):
        self.otp = OTPServices()

    def login_service(self, number):
        user = UserRepository.check_user_exists(number)
        if user and user.is_active:
            # todo:get password
            return
        else:
            self.otp.generate_otp_login(number)

    @staticmethod
    def user_authentication(number, password):
        return authenticate(number=number, password=password)

    def check_number_status(self, number):
        user = UserRepository.check_user_exists(number)
        if user and user.verified:
            return True
        elif user and user.verified is False:
            self.otp.generate_otp_login(number)
            return False
        else:
            account = UserRepository.insert_user_not_verified(number)
            self.otp.generate_otp_login(number)
            return False


class OTPServices:
    def __init__(self):
        self.redis_connection = get_redis_connection()

    def generate_otp_login(self, number):
        code = random.randint(100000, 999999)
        self.redis_connection.set(f'{number}_otp', code, ex=60 * 2)
        return
