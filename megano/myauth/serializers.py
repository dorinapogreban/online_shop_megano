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
        model = User  # Specificăm modelul asociat cu serializerul (dacă există)
        fields = ("id", "username", "password", "name")  # Specificăm câmpurile care trebuie incluse în serializare

    def validate(self, data):
        """
        Verifică dacă datele sunt valide.
        """
        # Verificați dacă username-ul este unic
        username = data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("This username is already in use.")

        # Alte verificări pot fi adăugate aici, cum ar fi validarea parolei

        return data


class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()  # тут возвращаем ссылку на изображение

    class Meta:
        model = Avatar
        fields = ["src", "alt"]
        # extra_kwargs = {'alt': {'required': False}}  # Permiteți valori goale pentru câmpul 'alt'

    def get_src(self, obj):
        return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения и/или обнавления профиля.
    Доступ имеет только авторизованный пользователь."""

    avatar = AvatarSerializer()  # тут берем сериалайзер аватарки

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]  # тут видим описали только те поля которые мы возвращаем

    def update(self, instance, validated_data):
        # Parsați și actualizați datele primite pentru câmpurile nested
        avatar_data = validated_data.pop('avatar', None)
        if avatar_data:
            # Actualizați avatarul folosind serializerul AvatarSerializer
            avatar_serializer = self.fields['avatar']
            avatar_instance = instance.avatar
            avatar_serializer.update(avatar_instance, avatar_data)
        # Actualizați restul câmpurilor profile
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
