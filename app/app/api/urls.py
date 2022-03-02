from django.urls import path
from .views import (
    ConfirmPasswordView,
    ResetPasswordView,
    UserRegistrationView,
    LoginApiView,
    LogOutView,
)

urlpatterns = [
    path("login/", LoginApiView.as_view()),
    path("registration/", UserRegistrationView.as_view()),
    path("logout/", LogOutView.as_view()),
    path("reset/", ResetPasswordView.as_view()),
    path("confirm/<user_pk>/<token>/", ConfirmPasswordView.as_view()),
]
