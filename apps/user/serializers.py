from rest_framework import serializers

from .models import CustomUser


class CreateUserInputSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=255, required=True)


class CreateUserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "username", "first_name", "last_name", "is_admin", "is_active")


class UserInputUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, allow_blank=True, allow_null=True, required=True)
    first_name = serializers.CharField(max_length=255, allow_blank=True, allow_null=True, required=True)
    last_name = serializers.CharField(max_length=255, allow_blank=True, allow_null=True, required=True)
