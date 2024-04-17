from django.urls import path
from .views import (
    SignInView,
    SignUpView,
    SignOutView,
    ProfileView,
    ProfilePasswordUpdateView,
    ProfileAvatarUpdateView,

)


"""
Настраиваем маршруты URL, чтобы можно было обращаться к представлению для регистрации через API.
"""
app_name = "myauth"

urlpatterns = [
    path('sign-in', SignInView.as_view(), name="login"),
    path("sign-up", SignUpView.as_view(), name="register"),
    path('sign-out', SignOutView.as_view(), name="logout"),
    path("profile", ProfileView.as_view(), name="profile"),
    path("profile/password", ProfilePasswordUpdateView.as_view(), name="profile-password"),
    path("profile/avatar", ProfileAvatarUpdateView.as_view(), name="profile-avatar"),

]