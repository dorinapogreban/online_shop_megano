from django.contrib import admin
from .models import Profile, Avatar


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "fullName", "email", "phone", "avatar")
    list_display_links = "pk", "fullName"
    # ordering = "-title"
    search_fields = "user", "fullName", "email", "phone"


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ["src", "alt"]
