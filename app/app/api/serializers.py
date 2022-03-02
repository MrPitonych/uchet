from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RegistrationSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="email is used, please try different email",
            )
        ]
    )

    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="username is used, please try different username",
            )
        ]
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "confirm_password"]

    def validate(self, data):
        password = data["password"]
        confirm_password = data["confirm_password"]

        if password != confirm_password:
            raise serializers.ValidationError({"password": "passwords doesnt match. "})
        elif len(password) < 6:
            raise serializers.ValidationError(
                {"password": "passwords value should be 6 or more characters. "}
            )
        return data

    def save(self):

        user = User(username=self.validated_data["username"])
        user.email = self.validated_data["email"]
        user.set_password(self.validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=128, write_only=True)

    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        if username is None:
            raise serializers.ValidationError("username is required")

        if password is None:
            raise serializers.ValidationError("password is required")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("user not found")

        if not user.check_password(password):
            raise serializers.ValidationError("wrong password")

        token = Token.objects.get_or_create(user=user)[0]

        return {"username": username, "token": token}


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = ["email"]

        if email is None:
            raise serializers.ValidationError("email is required")

        return data
