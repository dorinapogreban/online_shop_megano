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

    name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ("id", "username", "password", "name")

    def validate(self, data):
        """
        Проверяе если данные валидны
        """
        # Проверка уникальности имени пользователя
        username = data.get("username")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("This username is already in use.")

        return data


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для аватара пользователя"""

    src = serializers.SerializerMethodField()  # тут возвращаем ссылку на изображение

    class Meta:
        model = Avatar
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения и/или обнавления профиля.
    Доступ имеет только авторизованный пользователь."""

    avatar = AvatarSerializer()  # тут берем сериалайзер аватарки

    class Meta:
        model = Profile
        fields = [
            "fullName",
            "email",
            "phone",
            "avatar",
        ]  # тут видим описали только те поля которые мы возвращаем

    def update(self, instance, validated_data):
        # Разбор и обновление полученных данных для вложенных полей
        avatar_data = validated_data.pop("avatar", None)
        if avatar_data:
            # Обновление аватара с использованием сериализатора AvatarSerializer
            avatar_serializer = self.fields["avatar"]
            avatar_instance = instance.avatar
            avatar_serializer.update(avatar_instance, avatar_data)
        return super().update(instance, validated_data)


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
