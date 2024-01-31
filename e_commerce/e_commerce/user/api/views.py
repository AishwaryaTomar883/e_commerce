from django.contrib.auth.models import Group
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView

from utils.messages import UserSignupMessages
from .serializers import LoginSerializer, SignupSerializer
from utils.base_utils import AppResponse, AuthService
from ..models import CarouselImage

app_response = AppResponse()


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)


def login(request):
    return render(request, "user/login.html")


class LoginAPIView(GenericAPIView):
    """
    API view for user login.
    """

    permission_classes = ()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle user login and authentication.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A success response containing authentication tokens on successful login.
                    An error response on failure.

        Raises:
            ValidationError: If the serializer validation fails.
            Exception: If any other exception occurs during the login process.
        """
        try:
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            return app_response.success(
                **AuthService().get_auth_tokens_for_user(serializer.validated_data),
            )
        except ValidationError as e:
            raise e
        except Exception as e:
            return app_response.error(messages=str(e))


def home(request):
    carousel_images = CarouselImage.objects.all()
    return render(request, "user/home.html", {"carousel_images": carousel_images})


def register(request):
    groups = Group.objects.all()
    return render(request, "user/register.html", {"groups": groups})


class RegistrationAPIView(CreateAPIView):
    """
    API view for User registration
    """

    serializer_class = SignupSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        """
        Create a new User instance.
        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Raises:
            ValidationError: If the serializer validation fails.
            Exception: If any other exception occurs during the creation process.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return app_response.success(messages=UserSignupMessages.SUCCESS_MESSAGE)
        except ValidationError as e:
            raise e
        except Exception as e:
            return app_response.error(messages=str(e))
