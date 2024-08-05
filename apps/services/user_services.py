import random
import datetime
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from apps.repositories.user_repositories import UserRepository
from apps.core.exceptions import UserPassInvalid, NumberInvalid
from apps.user.redis import OTPRedis


class UserServices:
    def __init__(self):
        self.otp = OTPServices()
        self.user_repo = UserRepository()

    @staticmethod
    def user_authentication(number, password):
        return authenticate(number=number, password=password)

    def login_user(self, number, password):
        user = self.user_repo.check_user_exists(number)
        if user is None:
            raise NumberInvalid
        user = self.user_authentication(number, password)
        if user:
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        else:
            # todo:check limit
            raise UserPassInvalid

    def check_number_status(self, number):
        user = self.user_repo.check_user_exists(number)
        if user and user.is_verified:
            return True
        elif user and user.is_verified is False:
            self.otp.generate_otp_login(number)
            return False
        else:
            UserRepository.insert_user_not_verified(number)
            self.otp.generate_otp_login(number)
            return False

    def verify_number(self, number, code):
        otp = self.otp.get_otp(f'{number}_otp')
        if otp is None:
            raise  # todo:handle exception

        print(otp)


class OTPServices:
    def __init__(self):
        self.redis = OTPRedis()

    def generate_otp_login(self, number):
        code = random.randint(100000, 999999)
        self.redis.insert(key=f'{number}_otp', expire_datetime=datetime.timedelta(minutes=2), value=code)
        return

    def get_otp(self, key):
        code = self.redis.get_key(key)
        return code
