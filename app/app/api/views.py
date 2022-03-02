from secrets import token_urlsafe
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from .serializers import EmailSerializer, LoginSerializer, RegistrationSerializer
from django.core.cache import cache
from django.conf import settings
from django.core.mail import send_mail


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=200)


class LogOutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "logout success"}, status=200)
        except User.DoesNotExist:
            return Response({"message": "user unauthorized"}, status=401)


class ResetPasswordView(APIView):

    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        email = request.data.get("email", None)

        if email is None:
            raise serializers.ValidationError("email is required")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("email not found")

        confirm_token = token_urlsafe(16)
        cache.set(user.pk, confirm_token, settings.REDIS_TIMEOUTS["RESET_PASSWORD"])

        message = f"to confirm the password change, follow the link: http://localhost:8000/api/auth/confirm/{user.pk}/{confirm_token}/"

        send_mail("Change Password", message, settings.EMAIL_HOST_USER, [user.email])
        return Response({"message": "check your mail to confirm change your password"})


class ConfirmPasswordView(APIView):

    permission_classes = [AllowAny]

    @staticmethod
    def get(request, user_pk, token):
        if user_pk not in cache or cache.get(user_pk) != token:
            return Response("lifetime of link has expired", status=400)

        try:
            user = User.objects.get(pk=user_pk)
            new_password = User.objects.make_random_password()
            user.set_password(new_password)
            user.save()
            cache.delete(user_pk)
            send_mail(
                "New Password",
                f"New Password: {new_password}",
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            return Response(status=200)
        except User.DoesNotExist:
            return Response(status=400)
