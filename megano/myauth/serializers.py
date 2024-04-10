from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Avatar, Profile


class SignInSerializer(serializers.ModelSerializer):
    """
    Определяем сериализатор, который будет использоваться для проверки и валидации данных входа пользователя.
    """
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "password")


class SignUpSerializer(serializers.ModelSerializer):
    """
    Определяем сериализатор, который будет использоваться для проверки и валидации данных регистрации пользователя.
    """
    name = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "password", "name")


# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     fullname = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = User
#         fields = ("id", "username", "password", "fullname")
#         extra_kwargs = {"password": {"write_only": True}}
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username']
#         )
#         user.set_password(validated_data['password'])
#         user.save
#
#         fullname = validated_data['fullname']
#         profile = Profile.objects.create(
#             user=user,
#             fullname=fullname
#         )
#
#         return user


class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField() #тут возвращаем ссылку на изображение

    class Meta:
        model = Avatar
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения и/или обнавления профиля.
    Доступ имеет только авторизованный пользователь."""

    avatar = AvatarSerializer() #тут берем сериалайзер аватарки

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"] #тут видим описали только те поля которые мы возвращаем


class ProfileAvatarSerializer(serializers.ModelSerializer):
    """Сериалайзер для обнавления аватара пользователя"""

    class Meta:
        model = Profile
        fields = ["avatar"]


class ProfilePasswordSerializer(serializers.ModelSerializer):
    """Сериалайзер для обнавления пароля пользователя"""

    class Meta:
        model = Profile
        fields = ["password"]