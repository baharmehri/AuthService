from rest_framework import serializers
from apps.core.serializer_fields import PhoneNumberField
from apps.user.models import CustomUser


class LoginSerializer(serializers.Serializer):
    number = PhoneNumberField(required=True)
    password = serializers.CharField()


class NumberStatusSerializer(serializers.Serializer):
    number = PhoneNumberField(required=True)


class VerifyNumberSerializer(serializers.Serializer):
    number = PhoneNumberField(required=True)
    code = serializers.CharField(max_length=6, min_length=6, required=True)


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']


class UserOutputModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'number', 'first_name', 'last_name', 'email', 'is_active', 'is_verified')
