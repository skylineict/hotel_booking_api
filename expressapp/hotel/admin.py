""" This module contains the admin model for managing user authentication. """

from django.contrib import admin
from .models import Hotel


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    """
    A custom admin model for managing hotels in the system.
    """

    list_display = (
        "name",
        "address",
        "city",
        "country",
        "phone_number",
        "email",
        "status",
    )
