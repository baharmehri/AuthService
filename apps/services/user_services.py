import random
import datetime

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from apps.repositories.user_repositories import UserRepository as UserRepo
from apps.core.exceptions import UserPassInvalid, NumberInvalid, OTPInvalid
from apps.user.redis import OTPRedis
from apps.user.models import CustomUser


class UserServices:
    def __init__(self):
        self.otp = OTPServices()

    @staticmethod
    def user_authentication(number, password):
        return authenticate(number=number, password=password)

    @staticmethod
    def get_tokens(user: CustomUser):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def login_user(self, number, password):
        user = UserRepo.check_user_exists(number)
        if user is None:
            raise NumberInvalid
        user = self.user_authentication(number, password)
        if user:
            tokens = self.get_tokens(user)
            return tokens
        else:
            # todo:check limit
            raise UserPassInvalid

    def check_number_status(self, number):
        user = UserRepo.check_user_exists(number)
        if user and user.is_verified:
            return True
        elif user and user.is_verified is False:
            self.otp.generate_otp_login(number)
            return False
        else:
            UserRepo.insert_user_not_verified(number)
            self.otp.generate_otp_login(number)
            return False

    def verify_number(self, number, code):
        key_otp = f'{number}_otp'
        otp = self.otp.get_otp(key_otp)
        if otp is None:
            raise  # todo:handle exception
        if int(code) != int(otp):
            # todo:raise otp incorrect | add otp incorrect in redis
            raise OTPInvalid
        self.otp.expire_otp(key_otp)
        user = UserRepo.verify_number(number=number)
        tokens = self.get_tokens(user)
        return tokens


class OTPServices:
    def __init__(self):
        self.redis = OTPRedis()

    def generate_otp_login(self, number):
        code = random.randint(100000, 999999)
        self.redis.insert(key=f'{number}_otp', expire_datetime=datetime.timedelta(minutes=2), value=code)
        print(code)
        return

    def get_otp(self, key):
        code = self.redis.get_key(key)
        return code

    def expire_otp(self, key):
        return self.redis.remove_key(key)
