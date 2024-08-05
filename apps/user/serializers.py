from rest_framework import serializers
from apps.core.serializer_fields import PhoneNumberField


class LoginSerializer(serializers.Serializer):
    number = PhoneNumberField(required=True)
    password = serializers.CharField()


class NumberStatusSerializer(serializers.Serializer):
    number = PhoneNumberField(required=True)


class VerifyNumberSerializer(serializers.Serializer):
    number = PhoneNumberField(required=True)
    code = serializers.CharField(max_length=6, min_length=6, required=True)
