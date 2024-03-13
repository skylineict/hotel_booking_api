""" This module contains the custom user model for the application. """

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .usermanager import CustomUsermanager
from .utils import generate_username


class CustomUser(AbstractBaseUser):
    """
    Custom user model representing a user in the system.
    """

    id = models.CharField(
        primary_key=True,
        max_length=12,
        editable=False,
        default=generate_username,
    )
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(
        _("username"), unique=True, null=True, blank=True, max_length=100
    )
    phone = models.CharField(
        _("phone number"), unique=True, null=True, blank=True, max_length=15
    )
    otp = models.CharField(_("otp"), max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(_("otp expiry"), null=True, blank=True)
    is_active = models.BooleanField(_("active"), default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CustomUsermanager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        """
        Meta class for defining metadata options for the User model.
        """

        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):  # pylint: disable=unused-argument
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):  # pylint: disable=unused-argument
        "Does the user have permissions to view the app `app_label`?"
        return True
