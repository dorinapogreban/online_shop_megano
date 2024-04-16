from django.db import models
from django.contrib.auth.models import User


class Avatar(models.Model):
    """Модель для хранения аватара пользователя"""

    src = models.ImageField(
        upload_to="app_users/avatars/user_avatars/",
        default="app_users/avatars/default.png",
        verbose_name="Link",
        blank=True,
        null=True,
    )
    alt = models.CharField(max_length=128, blank=True, null=True,  verbose_name="Description")

    class Meta:
        verbose_name = "Avatar"
        verbose_name_plural = "Avatars"


class Profile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    fullName = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name="Phone")
    avatar = models.ForeignKey(
        Avatar,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Avatar",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"