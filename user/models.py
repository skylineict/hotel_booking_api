""" This module contains the custom user model for the application. """

from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from shortuuid.django_fields import ShortUUIDField

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
    is_vendor = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    verification_otp = models.CharField(max_length=6, blank=True)
    verification_otp_expiration = models.DateTimeField(null=True)
    reset_password_otp = models.CharField(max_length=6, blank=True)
    reset_password_otp_expiration = models.DateTimeField(null=True)

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
        if not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def generate_verification_otp(self):
        """Send OTP to the user."""
        otp = generate_otp()
        self.verification_otp = otp
        self.verification_otp_expiration = timezone.now() + timezone.timedelta(
            minutes=30
        )
        self.is_active = True
        self.save()
        send_mail(
            "JE Express Account Activation",
            f"Your OTP is {otp}. Use it to activate your account.",
            None,
            [self.email],
        )
