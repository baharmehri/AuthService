from rest_framework import serializers
from apps.base.base_serializers import BaseInputSerializer


class LoginSerializer(BaseInputSerializer):
    number = serializers.CharField(max_length=11, min_length=11, required=True)
    password = serializers.CharField()


class NumberStatusSerializer(BaseInputSerializer):
    number = serializers.CharField(max_length=11, min_length=11, required=True)
