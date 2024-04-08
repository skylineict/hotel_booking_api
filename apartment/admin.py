""" This module contains the admin model for managing apartments in the system. """

from django.contrib import admin
from .models import Apartment


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    """
    A custom admin model for managing apartments in the system.
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
