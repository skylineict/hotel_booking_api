""" This module contains the custom user model for the application. """

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField

from .usermanager import Usermanager


class User(AbstractBaseUser):
    """
    User model representing a user in the system.
    """

    id = ShortUUIDField(
        unique=True,
        primary_key=True,
        max_length=20,
        alphabet="abcdefghijklmnopqrstuvwxyz0123456789",
        prefix="usr-",
        editable=False,
    )
    firstname = models.CharField(_("first name"), max_length=50, null=True)
    lastname = models.CharField(_("last name"), max_length=50, null=True)
    username = models.CharField(_("username"), unique=True, max_length=20)
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(_("phone number"), unique=True, null=True, max_length=15)
    dob = models.DateField(_("date of birth"), null=True)
    is_vendor = models.BooleanField(_("vendor"), default=True)
    is_active = models.BooleanField(_("active"), default=False)
    otp = models.CharField(_("otp"), max_length=6, null=True)
    otp_expiry = models.DateTimeField(_("otp expiry"), null=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = Usermanager()

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
