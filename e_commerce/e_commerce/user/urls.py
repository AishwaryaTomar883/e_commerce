from django.urls import path, include

from .views import (
    UserDetailView,
    UserRedirectView,
    UserUpdateView,
)

app_name = "user"
urlpatterns = [
    path("redirect/", view=UserRedirectView.as_view(), name="redirect"),
    path("update/", view=UserUpdateView.as_view(), name="update"),
    path("<str:username>/", view=UserDetailView.as_view(), name="detail"),
    path("api/v1/", include("user.api.urls", namespace="user_api")),
]
