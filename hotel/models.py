""" This module contains the custom user model for the application. """

from django.db import models
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField

from user.models import User
from image.models import Image


class Hotel(models.Model):
    """Custom hotel model representing a hotel in the system."""

    hotel_id = ShortUUIDField(
        unique=True,
        prefix="hotl-",
        max_length=20,
        alphabet="abcdefghijklmnopqrstuvwxyz0123456789",
        editable=False,
        primary_key=True,
    )
    name = models.CharField(max_length=255)
    featured_image = models.ForeignKey(Image, on_delete=models.DO_NOTHING, related_name="featured_image")
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=255, unique=True)
    registration_status = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hotels")
    is_active = models.BooleanField(default=False)
    date_registered = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        """Meta class for defining metadata options for the Hotel model."""

        verbose_name = _("hotel")
        verbose_name_plural = _("hotels")

    def __str__(self):
        return str(self.name)


class Facility(models.Model):
    """Facility model representing a facility in a hotel."""

    id = models.CharField(primary_key=True, max_length=255, editable=False)
    label = models.CharField(max_length=255, unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        self.id = self.label.replace(" ", "").lower().replace("_", "")
        return super().save(*args, **kwargs)


class HotelFacility(models.Model):
    """HotelFacility model representing a facility in a hotel."""

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    objects = models.Manager()


# class HotelRoom(models.Model):
#     """Custom hotel room model representing a room in a hotel."""

#     room_id = ShortUUIDField(
#         unique=True,
#         prefix="room-",
#         max_length=20,
#         alphabet="abcdefghijklmnopqrstuvwxyz0123456789",
#         editable=False,
#         primary_key=True,
#     )
#     hotel = models.ForeignKey(
#         Hotel, on_delete=models.CASCADE, related_name="rooms"
#     )
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     image = models.URLField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     max_guests = models.PositiveIntegerField()
#     is_active = models.BooleanField(default=True)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)

#     objects = models.Manager()

#     class Meta:
#         """Meta class for defining metadata options for the HotelRoom model."""

#         verbose_name = _("hotel room")
#         verbose_name_plural = _("hotel rooms")

#     def __str__(self):
#         return str(self.name)

#     def save(self, *args, **kwargs):
#         return super().save(*args, **kwargs)


# class HotelBooking(models.Model):
#     """Custom hotel booking model representing a booking in a hotel."""

#     booking_id = ShortUUIDField(
#         unique=True,
#         prefix="book-",
#         max_length=20,
#         alphabet="abcdefghijklmnopqrstuvwxyz0123456789",
#         editable=False,
#         primary_key=True,
#     )
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="bookings"
#     )
#     room = models.ForeignKey(
#         HotelRoom, on_delete=models.CASCADE, related_name="bookings"
#     )
#     check_in = models.DateTimeField()
#     check_out = models.DateTimeField()
#     guests = models.PositiveIntegerField()
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     date_booked = models.DateTimeField(auto_now_add=True)

#     objects = models.Manager()

#     class Meta:
#         """Meta class for defining metadata options for the HotelBooking model."""

#         verbose_name = _("hotel booking")
#         verbose_name_plural = _("hotel bookings")

#     def __str__(self):
#         return str(self.booking_id)

#     def save(self, *args, **kwargs):
#         return super().save(*args, **kwargs)


# class HotelReview(models.Model):
#     """Custom hotel review model representing a review of a hotel."""

#     review_id = ShortUUIDField(
#         unique=True,
#         prefix="revw-",
#         max_length=20,
#         alphabet="abcdefghijklmnopqrstuvwxyz0123456789",
#         editable=False,
#         primary_key=True,
#     )
#     hotel = models.ForeignKey(
#         Hotel, on_delete=models.CASCADE, related_name="reviews"
#     )
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="reviews"
#     )
#     rating = models.PositiveIntegerField()
#     review = models.TextField()
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)

#     objects = models.Manager()

#     class Meta:
#         """Meta class for defining metadata options for the HotelReview model."""

#         verbose_name = _("hotel review")
#         verbose_name_plural = _("hotel reviews")

#     def __str__(self):
#         return str(self.review_id)

#     def save(self, *args, **kwargs):
#         return super().save(*args, **kwargs)
