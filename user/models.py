""" This module contains the custom user model for the application. """

import string
import random
from django.utils import timezone
from django.template.loader import render_to_string
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from mailqueue.models import MailerMessage

from user.usermanager import Usermanager
from user.utils import generate_otp


class User(AbstractBaseUser):
    """
    User model representing a user in the system.
    """

    GENDERS = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    id = ShortUUIDField(
        primary_key=True,
        max_length=16,
        alphabet="abcdefghijklmnopqrstuvwxyz0123456789",
        prefix="usr-",
        editable=False,
    )
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    username = models.CharField(unique=True, max_length=20)
    email = models.EmailField(unique=True)
    phone = models.CharField(unique=True, null=True, max_length=15)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDERS)
    is_vendor = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    verification_otp = models.CharField(max_length=6, blank=True, null=True)
    verification_otp_expiration = models.DateTimeField(null=True)
    reset_password_otp = models.CharField(max_length=6, blank=True, null=True)
    reset_password_otp_expiration = models.DateTimeField(null=True)
    is_suspended = models.BooleanField(default=False)

    objects = Usermanager()

    USERNAME_FIELD = "email"

    class Meta:
        """
        Meta class for defining metadata options for the User model.
        """

        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_sha256$"):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def generate_verification_otp(self):
        """Send OTP to the user."""
        otp = generate_otp()
        self.verification_otp = otp
        self.verification_otp_expiration = timezone.now() + timezone.timedelta(
            minutes=5
        )
        self.save()
        context = {
            "firstname": self.firstname,
            "verification_otp": self.verification_otp,
        }
        message = render_to_string("verification.html", context)
        msg = MailerMessage()
        msg.subject = "JE Express Account Activation"
        msg.to_address = self.email
        msg.from_address = "JE Express <yiradesat@gmal.com>"
        msg.content = message
        msg.html_content = message
        msg.save()

    def generate_reset_password_otp(self):
        """Generate OTP for resetting password."""
        otp = generate_otp()
        self.reset_password_otp = otp
        self.reset_password_otp_expiration = timezone.now() + timezone.timedelta(
            minutes=5
        )
        self.save()
        context = {
            "firstname": self.firstname,
            "reset_password_otp": self.reset_password_otp,
        }
        message = render_to_string("reset_password.html", context)
        msg = MailerMessage()
        msg.subject = "JE Express Reset Password"
        msg.to_address = self.email
        msg.from_address = "JE Express <yiradesat@gmal.com>"
        msg.content = message
        msg.html_content = message
        msg.save()


class ResetPassword(models.Model):
    """Reset Password Model."""

    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, editable=False
    )
    reset_password_token = models.CharField(
        max_length=24,
    )
    expiration_time = models.DateTimeField()

    objects = models.Manager()

    class Meta:
        """Metadata for the Reset Password model."""

        verbose_name = "reset_password"

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        allowed_chars = "".join((string.ascii_letters, string.digits))
        self.reset_password_token = "".join(
            random.choice(allowed_chars) for _ in range(20)
        )
        self.expiration_time = timezone.now() + timezone.timedelta(minutes=5)
        return super().save(*args, **kwargs)
