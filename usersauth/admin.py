""" This module contains the admin model for managing user authentication. """

from django.contrib import admin
from .models import User


@admin.register(User)
class Useradmin(admin.ModelAdmin):
    """
    A class used to represent the User model in the admin interface.
    """

    list_display = [
        "email",
        "username",
        "phone",
        "is_active",
        "date_joined",
    ]
