from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    def create(self, validated_data):
        del validated_data["password2"]
        return User.objects.create_user(**validated_data)

    def validate_username(self, value):
        if value == "admin":
            raise serializers.ValidationError("username cant be admin")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("passwords must match")
        return data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = User.objects.filter(username=username).first()

            if user and user.check_password(password):

                refresh = RefreshToken.for_user(user)
                return {
                    "username": user.username,
                    "token": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                }
            else:
                raise serializers.ValidationError("Invalid username or password.")
        else:
            raise serializers.ValidationError("Username and password are required.")
