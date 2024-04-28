""" This module contains the hotel booking model for the application. """

from django.db import models
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField
from user.models import User


class HotelBooking(models.Model):
    """HotelBooking model representing a hotel booking in the system."""

    booking_id = ShortUUIDField(
        unique=True,
        length=12,
        max_length=20,
        alphabet="abcdefghijklmnopqrstuvwxyz0123456789",
        editable=False,
        primary_key=True,
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_booked = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    hotel = models.ForeignKey(
        "hotel.Hotel", on_delete=models.CASCADE, related_name="hotel_bookings"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="hotel_bookings"
    )
    salutation = models.CharField(max_length=10)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20, default="pending")

    objects = models.Manager()

    class Meta:
        """Meta class for defining metadata options for the HotelBooking model."""

        verbose_name = _("hotel booking")
        verbose_name_plural = _("hotel bookings")

    def __str__(self):
        return str(self.hotel)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
