from django.db import models
from django.contrib.auth.models import User


class Avatar(models.Model):
    """Модель для хранения аватара пользователя"""

    src = models.ImageField(
        upload_to="app_users/avatars/user_avatars/",
        default="app_users/avatars/default.png",
        verbose_name="Link",
    )
    alt = models.CharField(max_length=128, verbose_name="Description")

    class Meta:
        verbose_name = "Avatar"
        verbose_name_plural = "Avatars"


class Profile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    fullName = models.CharField(max_length=128, blank=True, null=True, verbose_name="Full name")
    phone = models.PositiveIntegerField(
        blank=True, null=True, unique=True, verbose_name="Phone number"
    )
    balance = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, verbose_name="Balance"
    )
    # email = models.EmailField(verbose_name="Email", unique=True)
    avatar = models.ForeignKey(
        Avatar,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Avatar",
    )