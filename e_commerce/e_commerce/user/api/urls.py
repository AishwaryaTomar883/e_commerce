from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import CustomTokenRefreshView, login, LoginAPIView, home, register, RegistrationAPIView

app_name = "user_api"

router = SimpleRouter()

urlpatterns = router.urls

urlpatterns += [
    path("refresh-token/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("login/", login, name="login"),
    path("login_api/", LoginAPIView.as_view(), name="login_api"),
    path("home/", home, name="home"),
    path("register/", register, name="register"),
    path("register_api/", RegistrationAPIView.as_view(), name="register_api"),
]
