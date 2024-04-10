from django.urls import path
from .views import (
    SignInView,
    SignUpView,
    signOut,
    ProfileView,
    # ListUsers,
    # edit_profile
)

# router = routers.DefaultRouter()
# router.register(r"api", SignUpView)

"""
Настраиваем маршруты URL, чтобы можно было обращаться к представлению для регистрации через API.
"""
app_name = "myauth"

urlpatterns = [
    # path(
    #         "sign-in/",
    #         SignInView.as_view(
    #             template_name="myauth/login.html",
    #             redirect_authenticated_user=True,
    #         ),
    #         name="login",
    #     ),

    #  SignInView.as_view(), name="sign-in"

    path('sign-in/', SignInView.as_view(), name="login"),
    path("sign-up/", SignUpView.as_view(), name="register"),
    path('sign-out/', signOut, name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/password/", ProfileView.as_view(), name="profile"),
    path("profile/avatar/", ProfileView.as_view(), name="profile"),
    # path("users/", ListUsers.as_view(), name="list_users"),

    # path('edit_profile/', edit_profile, name='edit_profile'),
]