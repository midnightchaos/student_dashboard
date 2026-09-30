from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff")
    list_filter = ("role",)
    fieldsets = UserAdmin.fieldsets + (("Extra", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Extra", {"fields": ("role",)}),)
