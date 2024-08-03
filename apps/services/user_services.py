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
            code = random.randint(100000, 999999)
            self.otp.otp_login(number, code)

    @staticmethod
    def user_authentication(number, password):
        return authenticate(number=number, password=password)


class OTPServices:
    def __init__(self):
        self.redis_connection = get_redis_connection()

    def otp_login(self, number, code):
        self.redis_connection.set(f'{number}_otp', code, ex=60 * 2)
        return
