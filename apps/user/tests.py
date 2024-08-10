from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from apps.user.models import CustomUser
from apps.user.services import CacheServices, OTPService


class UserTestCase(TestCase):

    def setUp(self):
        CacheServices().redis.redis.flushdb()
        self.client = APIClient()
        self.url_prefix = '/api/v1'
        self.cache_services = CacheServices()
        self.otp_service = OTPService()
        self.user_verified = CustomUser.objects.create_user(number="09104562312", password="1234", is_verified=True)

    def test_phone_number_status_true(self):
        data = {
            "number": self.user_verified.number,
        }
        response = self.client.post(f'{self.url_prefix}/check-number', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_phone_number_status_false(self):
        data = {
            "number": "09104562313",
        }
        response = self.client.post(f'{self.url_prefix}/check-number', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        otp = self.cache_services.get_item(f'{data.get("number")}_otp')
        print(otp)
        self.cache_services.remove_item(f'{data.get("number")}_otp')

    def test_login_verified_user(self):
        data = {
            "number": self.user_verified.number,
            "password": "1234"
        }
        response = self.client.post(f'{self.url_prefix}/login', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_login_unverified_user(self):
        user = CustomUser.objects.create_user(number="09104562319")
        data = {
            "number": user.number,
            "password": "1234"
        }
        response = self.client.post(f'{self.url_prefix}/login', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(response.data)

    def test_verify_user_by_valid_otp(self):
        data = {
            "number": "09104562313",
            "code": ""
        }
        CustomUser.objects.create_user(number="09104562313", password="1234")

        otp = self.otp_service.generate_random_otp()
        self.cache_services.insert_item(f'{data.get("number")}_otp', otp, 60)

        data["code"] = otp

        response = self.client.post(f'{self.url_prefix}/verify', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.cache_services.remove_item(f'{data.get("number")}_otp')

    def test_verify_user_by_invalid_otp(self):
        data = {
            "number": "09104562313",
            "code": "123456"
        }
        CustomUser.objects.create_user(number="09104562313", password="1234")

        otp = self.otp_service.generate_random_otp()
        self.cache_services.insert_item(f'{data.get("number")}_otp', otp, 60)
        print("valid_otp", otp)
        response = self.client.post(f'{self.url_prefix}/verify', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.cache_services.remove_item(f'{data.get("number")}_otp')

    def test_reached_limit_otp(self):
        user = CustomUser.objects.create_user(number="09104562313")
        data = {
            "number": user.number,
            "code": "123456"
        }

        otp = self.otp_service.generate_random_otp()
        self.cache_services.insert_item(f'{data.get("number")}_otp', otp, 60)
        print("valid_otp", otp)
        for attempt in range(3):
            response = self.client.post(f'{self.url_prefix}/verify', data, format='json')
            if attempt == 3:
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                print(response.data)
                self.cache_services.remove_item(f'{data.get("number")}_otp')
                self.cache_services.remove_item(f'{data.get("number")}_attempt')
                self.cache_services.remove_item(f'2_127.0.0.1_attempt')
                break
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_set_password_new_user(self):
        user = CustomUser.objects.create_user(number="09123654589", is_verified=True)
        data = {
            "password": "123456"
        }
        token_user = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token_user))
        response = self.client.post(f'{self.url_prefix}/set-password', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
