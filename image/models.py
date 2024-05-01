""" This module contains the image model for the application. """

from django.db import models
from cloudinary.models import CloudinaryField


class Image(models.Model):
    """Image model representing an image in the system."""

    url = models.URLField(primary_key=True)
    image = CloudinaryField("image")

    def __str__(self):
        return str(self.url)

    def save(self, *args, **kwargs):
        self.url = (
            "https://res.cloudinary.com/destinedcodes/image/upload/"
            + str(self.image)
        )
        super().save(*args, **kwargs)

    class Meta:
        """Meta class for defining metadata options for the Image model."""

        verbose_name = "image"
        verbose_name_plural = "images"
