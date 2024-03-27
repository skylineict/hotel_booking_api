""" This module contains the apartment model for the application. """

from django.db import models
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField

from usersauth.models import CustomUser


class Apartment(models.Model):
    """Apartment model representing a hotel in the system."""

    apartment_id = ShortUUIDField(
        unique=True,
        length=12,
        prefix="apart-",
        max_length=20,
        alphabet="abcdefghijklmnopqrstuvwxyz0123456789",
        editable=False,
        primary_key=True,
    )
    agent = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="apartments"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    featured_image = models.URLField()
    images = models.JSONField(null=True, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    agent_registration_id = models.CharField(max_length=255, unique=True)
    registration_status = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.PositiveIntegerField()
    date_registered = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # TODO: Add Details and Amenities fields

    objects = models.Manager()

    class Meta:
        """Meta class for defining metadata options for the Hotel model."""

        verbose_name = _("aprtment")
        verbose_name_plural = _("apartments")

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

