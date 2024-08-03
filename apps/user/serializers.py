import re

from rest_framework import serializers
from apps.user.models import CustomUser


class LoginSerializer:
    class InputLoginSerializer(serializers.Serializer):
        number = serializers.CharField(
            max_length=11,
            min_length=11,
            required=True,
            help_text="A phone number consisting of exactly 11 digits."
        )
        password = serializers.CharField()

        def validate_number(self, number):
            phone_regex = '^09\d{9}$'
            if not re.match(phone_regex, number):
                raise serializers.ValidationError("Invalid phone number")
            return number
