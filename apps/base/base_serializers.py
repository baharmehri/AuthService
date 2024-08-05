from rest_framework import serializers
import re


class BaseInputSerializer(serializers.Serializer):
    def validate_number(self, number):
        phone_regex = '^09\d{9}$'
        if not re.match(phone_regex, number):
            raise serializers.ValidationError("Invalid phone number")
        return number
