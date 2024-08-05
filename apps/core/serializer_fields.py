import re

from rest_framework import serializers


class PhoneNumberField(serializers.CharField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self, value):
        phone_regex = '^09\d{9}$'
        if not re.match(phone_regex, value):
            raise serializers.ValidationError("Invalid phone number")
        return value
