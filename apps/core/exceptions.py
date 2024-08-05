from django.core.exceptions import ValidationError


class UserPassInvalid(Exception):
    def __init__(self, message="Username or password is incorrect."):
        self.message = message
        super().__init__(self.message)
        self.http_code = 404


class NumberInvalid(Exception):
    def __init__(self, message="Number is invalid."):
        self.message = message
        super().__init__(self.message)
        self.http_code = 404


class OTPInvalid(Exception):
    def __init__(self, message="Invalid OTP code."):
        self.message = message
        super().__init__(self.message)
        self.http_code = 404
