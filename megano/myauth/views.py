from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User

from rest_framework import status, permissions
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from .models import Profile, Avatar
from .serializers import ProfileSerializer, ProfileAvatarSerializer


class SignInView(APIView):
    """
     Cоздаём представление, которое будет обрабатывать запрос
      на вход в систему и проверять учетные данные пользователя.
    """

    def post(self, request: Request) -> Response:
        serialized_data = list(request.POST.keys())[0]
        user_data = json.loads(serialized_data)
        username = user_data.get("username")
        password = user_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    """
    Cоздаём представление, которое будет обрабатывать запрос на регистрацию нового пользователя.
    """
    def post(self, request) -> Response:
        serialized_data = list(request.data.keys())[0]
        user_data = json.loads(serialized_data)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")
        try:
            user = User.objects.create_user(username=username, password=password)
            profile = Profile.objects.create(user=user, fullName=name)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignOutView(APIView):
    """
     Cоздаём представление, которое будет обрабатывать запрос
      на выход пользователя из системы.
    """
    def post(self, request):
        # Выход пользователя
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    """
    Представления для получения и/или обнавления профиля.
    Доступ имеет только авторизованный пользователь.
    """

    serializer_class = ProfileSerializer
    parser_classes = (FormParser, MultiPartParser, JSONParser)
    permission_classes = [permissions.IsAuthenticated] #пишем пермиш потому что сюда не авторизованные заходить не могут

    def test_func(self):
        return self.request.user.is_authenticated

    def get(self, request) -> Response:
        """
        Получает профиль пользователя.
        """
        profile = request.user.profile  #достаем профиль
        serializer = ProfileSerializer(profile, many=False) #отправляем объект в сериалайзер чтобы привести в формат который ждет фронт
        return Response(serializer.data, status=status.HTTP_200_OK) #возвращаем данные

    def post(self, request) -> Response:
        """
        Обрабатывает POST-запрос для обновления профиля.
        """
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfilePasswordUpdateView(APIView):
    """Представления для обнавления пароля пользователя"""
    def post(self, request):
        """
        Обрабатывает POST-запрос для обновления пароля пользователя.
        """
        # Получаем профиль аутентифицированного пользователя
        profile_user = request.user.profile

        # Проверяем наличие пароля в запросе
        if profile_user.user.password:
            new_password = request.data.get('newPassword')
            # Устанавливаем новый пароль для пользователя, связанного с профилем
            profile_user.user.set_password(new_password)
            profile_user.user.save()
            # Обновляем сеанс аутентификации для использования нового пароля
            update_session_auth_hash(request, profile_user.user)

            # Сериализуем обновленный профиль и возвращаем ответ
            serializer = ProfileSerializer(profile_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Password field is required'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileAvatarUpdateView(UpdateAPIView):
    """Представления для обнавления аватара пользователя"""
    parser_classes = (MultiPartParser, JSONParser)
    def post(self, request):
        """
        Обрабатывает POST-запрос для обновления аватара пользователя.
        """
        # Получаем профиль аутентифицированного пользователя
        profile_user = request.user.profile
        # Проверяем наличие аватара для пользователя и удаляем его, если существует
        if profile_user.avatar:
            profile_user.avatar.delete()

        # Создаем новый объект Avatar с помощью загруженного файла
        new_avatar = Avatar.objects.create(src=request.FILES['avatar'])
        # Обновляем аватар пользователя в профиле
        profile_user.avatar = new_avatar
        profile_user.save()
        # Сериализуем обновленный профиль и возвращаем ответ
        serializer = ProfileAvatarSerializer(profile_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

