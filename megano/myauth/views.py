from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from django.core.checks import messages
# from django.shortcuts import render, redirect
from rest_framework import status, permissions, authentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import UpdateAPIView, CreateAPIView, ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

# from .forms import EditProfileForm
from .models import Profile
from .serializers import ProfileSerializer, SignInSerializer, SignUpSerializer, ProfileAvatarSerializer


# class SignInView(APIView):
#     def post(self, request: Request) -> Response:
#         serialized_data = list(request.POST.keys())[0]
#         user_data = json.loads(serialized_data)
#         username = user_data.get("username")
#         password = user_data.get("password")
#
#         user = authenticate(request, username=username, password=password)
#         print(user)
#         if user is not None:
#             login(request, user)
#             return Response(status=status.HTTP_201_CREATED)
#
#         return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SignInView(APIView):
    """
     Cоздаём представление, которое будет обрабатывать запрос
      на вход в систему и проверять учетные данные пользователя.
    """
    # model = User
    # serializel_class = SignInSerializer

    def post(self, request) -> Response:
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    """
    Cоздаём представление, которое будет обрабатывать запрос на регистрацию нового пользователя.
    """
    model = User
    serializel_class = SignInSerializer

    def post(self, request) -> Response:
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
                # Создаем нового пользователя
                user = User.objects.create_user(username=username, password=password)
                profile = Profile.objects.create(user=user, first_name=name)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            except Exception:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # serialized_data = list(request.data.keys())[0]
        # user_data = json.loads(serialized_data)
        # name = user_data.get("name")
        # username = user_data.get("username")
        # password = user_data.get("password")
        # try:
        #     user = User.objects.create_user(username=username, password=password)
        #     profile = Profile.objects.create(user=user, first_name=name)
        #     user = authenticate(request, username=username, password=password)
        #     if user is not None:
        #         login(request, user)
        #     return Response(status=status.HTTP_201_CREATED)
        # except Exception:
        #                 return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def signOut(request):
    """
     Cоздаём представление, которое будет обрабатывать запрос
      на выход пользователя из системы.
    """
    # Выход пользователя
    logout(request)
    return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    """
    Представления для получения и/или обнавления профиля.
    Доступ имеет только авторизованный пользователь.
    """

    serializer_class = ProfileSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [permissions.IsAuthenticated] #пишем пермиш потому что сюда не авторизованные заходить не могут

    def test_func(self):
        return self.request.user.is_authenticated

    def get(self, request) -> Response:
        profile = Profile.objects.get(user=request.user)  #достаем профиль
        serializer = ProfileSerializer(profile, many=False) #отправляем объект в сериалайзер чтобы привести в формат который ждет фронт
        return Response(serializer.data, status=status.HTTP_200_OK) #возвращаем данные

    def post(self, request) -> Response:

        #Далее тут описываем Post запрос который описан в контракте
        #это то присылает фронттак же смотрим в контракт
        #Данные нужно получить и сериализовать как с GET и после сохранить их ведь это изменения вот так это будет
        profile = Profile.objects.get(user=request.user) #достаем профиль
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfilePasswordUpdateView(APIView):
    """Представления для обнавления пароля пользователя"""

    def post(self, request: Request) -> Response:
        profile_user = Profile.objects.get(user=request.user)
        if profile_user.password:
            profile_user.password.delete()

        profile_user.password = request.FILES["password"]
        profile_user.password.save()
        serializer = ProfileAvatarSerializer(profile_user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileAvatarUpdateView(UpdateAPIView):
    """Представления для обнавления аватара пользователя"""

    def post(self, request: Request) -> Response:
        profile_user = Profile.objects.get(user=request.user)
        if profile_user.avatar:
            profile_user.avatar.delete()

        profile_user.avatar = request.FILES["avatar"]
        profile_user.avatar.save()
        serializer = ProfileAvatarSerializer(profile_user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class ListUsers(APIView):
#     """
#     View to list all users in the system.
#
#     * Requires token authentication.
#     * Only admin users are able to access this view.
#     """
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser]
#
#     def get(self, request, format=None):
#         """
#         Return a list of all users.
#         """
#         usernames = [user.username for user in User.objects.all()]
#         return Response(usernames)


# def edit_profile(request):
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = EditProfileForm(instance=request.user)
#     return render(request, 'edit_profile.html', {'form': form})