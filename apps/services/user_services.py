import os
import random
import datetime
import pytz
from abc import ABC, abstractmethod

from django.utils import timezone
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from kavenegar import KavenegarAPI, APIException, HTTPException

from apps.repositories.user_repositories import UserRepository as UserRepo, BannedIPRepository as BannedIPRepo
from apps.core.exceptions import UserPassInvalid, NumberInvalid, OTPInvalid, ReachedLimit
from apps.user.redis import CacheRedis
from apps.user.models import CustomUser


class UserServices:
    def __init__(self):
        self.cache_service = CacheServices()
        self.otp_service = OTPService()

    @staticmethod
    def user_authentication(user_password, input_password):
        return check_password(password=input_password, encoded=user_password)

    @staticmethod
    def get_tokens(user: CustomUser):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    @staticmethod
    def set_password_for_new_user(user, password) -> None:
        UserRepo.set_password(user.id, password)

    @staticmethod
    def is_user_reached_limit(user: CustomUser) -> bool:
        now = timezone.now().astimezone(pytz.UTC)
        if not user.banned_until or user.banned_until >= now:
            return False
        return True

    @staticmethod
    def is_ip_reached_limit(user: CustomUser, ip) -> bool:
        now = timezone.now().astimezone(pytz.UTC)
        banned_ip = BannedIPRepo.get_by_filter(user=user, ip=ip).first()
        if not banned_ip or banned_ip.banned_until >= now:
            return False
        return True

    def is_item_reached_limit(self, item) -> bool:
        try_count = self.cache_service.get_item(f'{item}_attempt')
        if not try_count or int(try_count) <= 3:
            return False
        return True

    def update_limit_count(self, item):
        cached_value = self.cache_service.get_item(f'{item}_attempt')
        try_count = int(cached_value) if cached_value else 0
        self.cache_service.insert_item(f'{item}_attempt', try_count + 1, 60)

    def check_reached_limit(self, user: CustomUser, ip):
        if self.is_ip_reached_limit(user, ip):
            raise ReachedLimit()

        if self.is_user_reached_limit(user):
            raise ReachedLimit()

        if self.is_item_reached_limit(user.number):
            UserRepo.ban_user(user, 60)
            raise ReachedLimit("User has reached the limit based on their number of attempts.")

        if self.is_item_reached_limit(f'{user.id}_{ip}'):
            BannedIPRepo.create(user=user, ip=ip)
            raise ReachedLimit("User has reached the limit based on their ip of attempts.")

    def login_user(self, validated_data, ip):
        number = validated_data.get("number")
        password = validated_data.get("password")
        user = UserRepo.check_user_exists(number)
        if user is None:
            raise NumberInvalid()

        self.check_reached_limit(user, ip)
        if not self.user_authentication(user_password=user.password, input_password=password):
            self.update_limit_count(number)
            self.update_limit_count(f'{user.id}_{ip}')
            raise UserPassInvalid()
        tokens = self.get_tokens(user)
        return tokens

    def generate_otp(self, number):
        code = self.otp_service.generate_random_otp()
        self.otp_service.verify_otp(code, number)
        self.cache_service.insert_item(f'{number}_otp', code, expire_minute=2)

    def check_number_status(self, number):
        user = UserRepo.check_user_exists(number)
        if user and user.is_verified:
            return True

        if not user:
            UserRepo.insert_user_not_verified(number)
        self.generate_otp(number)
        return False

    def verify_number(self, validated_data, ip):
        number = validated_data["number"]
        code = validated_data["code"]

        user = UserRepo.check_user_exists(number)
        if user is None:
            raise NumberInvalid()

        self.check_reached_limit(user, ip)

        key_otp = f'{number}_otp'
        otp = self.cache_service.get_item(key_otp)
        if otp is None:
            raise OTPInvalid

        if int(code) != int(otp):
            self.update_limit_count(number)
            self.update_limit_count(f'{user.id}_{ip}')
            raise OTPInvalid

        self.cache_service.remove_item(key_otp)
        user = UserRepo.verify_number(number=number)
        tokens = self.get_tokens(user)
        return tokens

    def update_profile(self, user, validated_data):
        profile = UserRepo.update(
            user,
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name")
        )
        return profile


class CacheServices:
    def __init__(self):
        self.redis = CacheRedis()

    def get_item(self, key):
        value = self.redis.get_key(key)
        if value:
            value = value.decode('utf-8')
        return value

    def insert_item(self, key, value, expire_minute: int):
        self.redis.insert(key=key, value=value, expire_datetime=datetime.timedelta(minutes=expire_minute))

    def remove_item(self, key):
        return self.redis.remove_key(key)


class OTPService(ABC):

    def generate_random_otp(self):
        code = random.randint(100000, 999999)
        return code

    def verify_otp(self, *args, **kwargs):
        pass


class KavenegarOTPService(OTPService):
    API_KEY = os.environ.get('KAVENEGAR_API_KEY')

    def verify_otp(self, code, receiver):
        try:
            api = KavenegarAPI(apikey=self.API_KEY)
            params = {
                'receptor': receiver,
                'template': 'otp',
                'token': code,
                'type': 'sms',
            }
            api.verify_lookup(params)
        except APIException as e:
            print(e)
        except HTTPException as e:
            print(e)
