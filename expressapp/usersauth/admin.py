""" This module contains the admin model for managing user authentication. """

from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUseradmin(admin.ModelAdmin):
    """
    A custom admin model for managing user authentication.
    """

    list_display = [
        "email",
        "username",
        "phone",
        "is_active",
        "date_joined",
    ]
