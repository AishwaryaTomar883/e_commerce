from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework import serializers
from utils.constants import AuthConstantsMessages
from utils.import_models import User
from utils.messages import UserSignupMessages
from utils.utils import normalize_email
from django.contrib.auth.password_validation import validate_password


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


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True, )
    role = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password", "confirm_password", "role"]
        extra_kwargs = {
            "username": {"required": False},
            "first_name": {"required": True, "allow_blank": False, },
            "last_name": {"required": True, "allow_blank": False, },
        }

    def validate_password(self, password: str) -> str:
        """
        Validation method for the 'password' field.
        Args:
            password (str): The password value to be validated.
        Returns:
            str: The validated password value.
        Raises:
            serializers.ValidationError: If the password does not match the 'confirm_password' field.
        """
        confirm_password = self.initial_data.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError(
                UserSignupMessages.PASSWORD_NOT_MATCH_ERROR
            )
        return password

    def validate_email(self, email: str) -> str:
        """
        Validation method for the 'email' field.
        Args:
            email (str): The email value to be validated.
        Returns:
            str: The validated email value.
        Raises:
            serializers.ValidationError: If the email already exists in the User model.
        """
        email = normalize_email(email)
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(UserSignupMessages.EMAIL_EXIST_ERROR)
        return email

    def validate_role(self, role: str) -> Group:
        """
        Validation method for the 'role' field.
        Args:
            role (str): The role name to be validated.
        Returns:
            group: The validated group name.
        Raises:
            serializers.ValidationError: If the role does not exist.
        """
        try:
            return Group.objects.get(name__iexact=role.lower())
        except Group.DoesNotExist:
            raise serializers.ValidationError(UserSignupMessages.INVALID_ROLE_ERROR)

    def create(self, validated_data: dict) -> User:
        """This method creates a new instance of the User model based on the validated data.
        Args:
            validated_data (dict): The validated data for creating the User.
        Returns:
            user: The created User instance.
        """
        role = validated_data.pop("role")
        password = validated_data.pop("password")
        validated_data.pop("confirm_password")
        email = normalize_email(validated_data.get("email"))
        validated_data.update({"username": email})
        user = super().create(validated_data)
        user.set_password(password)
        user.groups.add(role)
        user.save()
        return user
