from django.contrib.auth import authenticate
from rest_framework import serializers
from utils.constants import AuthConstantsMessages


class LoginSerializer(serializers.Serializer):
    """
    Serializer for Login
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        """
        Validate method for login serializer
        :param attrs: OrderedDict
        :return: user (User model instance)
        Raises:
            serializers.ValidationError: If the user entered wrong email id and password.
        """
        login_data = {
            "password": attrs.get("password"),
            "username": attrs.get("email").lower(),
        }
        user = authenticate(**login_data)
        if not user:
            raise serializers.ValidationError(
                AuthConstantsMessages.INVALID_EMAIL_OR_PASSWORD
            )
        return user
