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
        print('ok')
        serialized_data = list(request.POST.keys())[0]
        user_data = json.loads(serialized_data)
        username = user_data.get("username")
        password = user_data.get("password")

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print('succes')
            return Response(status=status.HTTP_201_CREATED)

        print('error')
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    """
    Cоздаём представление, которое будет обрабатывать запрос на регистрацию нового пользователя.
    """
    def post(self, request) -> Response:
        print('ok')
        serialized_data = list(request.data.keys())[0]
        user_data = json.loads(serialized_data)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")
        print('da')
        try:
            print('try')
            user = User.objects.create_user(username=username, password=password)
            print(user)
            profile = Profile.objects.create(user=user, fullName=name)
            print(profile)
            user = authenticate(request, username=username, password=password)
            print('authenticate')
            if user is not None:
                login(request, user)
                print('login')
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            print('error')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignOutView(APIView):
    """
     Cоздаём представление, которое будет обрабатывать запрос
      на выход пользователя из системы.
    """
    def post(self, request):
        # Выход пользователя
        print('ok')
        logout(request)
        print('yes')
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
        profile = request.user.profile  #достаем профиль
        serializer = ProfileSerializer(profile, many=False) #отправляем объект в сериалайзер чтобы привести в формат который ждет фронт
        return Response(serializer.data, status=status.HTTP_200_OK) #возвращаем данные

    def post(self, request) -> Response:

        #Далее тут описываем Post запрос который описан в контракте
        #это то присылает фронттак же смотрим в контракт
        #Данные нужно получить и сериализовать как с GET и после сохранить их ведь это изменения вот так это будет
        # profile = request.user.profile #достаем профиль
        profile = Profile.objects.get(user=request.user)
        print(profile)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        print(serializer)
        print(serializer.error_messages)

        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():
            print(serializer.is_valid())
            serializer.save()
            print('save')
            return Response(serializer.data)
        print('ok')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfilePasswordUpdateView(APIView):
    """Представления для обнавления пароля пользователя"""
    def post(self, request):
        # Obțineți profilul utilizatorului autentificat
        profile_user = request.user.profile

        # Verificați dacă parola există în cerere
        if profile_user.user.password:
            new_password = request.data.get('newPassword')
            # Setează noua parolă pentru utilizatorul asociat profilului
            profile_user.user.set_password(new_password)
            profile_user.user.save()
            # Actualizați sesiunea de autentificare pentru a folosi noua parolă
            update_session_auth_hash(request, profile_user.user)

            # Serializați profilul actualizat și returnați răspunsul
            serializer = ProfileSerializer(profile_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Password field is required'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileAvatarUpdateView(UpdateAPIView):
    """Представления для обнавления аватара пользователя"""
    parser_classes = (MultiPartParser, JSONParser)
    def post(self, request):
        # Obțineți profilul utilizatorului autentificat
        print(request.user)
        profile_user = request.user.profile
        print(profile_user)
        print(profile_user.user)
        print(profile_user.avatar)
        # Verificați dacă există deja un avatar pentru utilizator și ștergeți-l
        if profile_user.avatar:
            profile_user.avatar.delete()
            print('avatar dellete')

        # Creați un nou obiect Avatar folosind fișierul încărcat
        new_avatar = Avatar.objects.create(src=request.FILES['avatar'])
        print(new_avatar, "create")
        # Actualizați avatarul utilizatorului în profil
        profile_user.avatar = new_avatar
        profile_user.save()
        print(profile_user.avatar, "save")
        # Serializați profilul actualizat și returnați răspunsul
        serializer = ProfileAvatarSerializer(profile_user)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

