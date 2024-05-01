""" This module contains the custom user manager for the user model. """

from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class Usermanager(BaseUserManager):
    """
    Custom user manager for creating and managing user accounts.
    """

    def create_user(self, email, password, username=None, phone=None, **extra_fields):
        """
        Creates a new user with the given email, username, phone, and password.

        Args:
            email (str): The email address of the user.
            username (str, optional): The username of the user.
            phone (str, optional): The phone number of the user.
            password (str, optional): The password for the user.
            **extra_fields: Additional fields to be saved in the user model.

        Returns:
            User: The created user object.
        """
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_vendor(self, email, password, username=None, phone=None, **extra_fields):
        """
        Creates a vendor with the given email, username, phone, and password.

        Args:
            email (str): The email address of the vendor.
            username (str, optional): The username of the vendor.
            phone (str, optional): The phone number of the vendor.
            password (str, optional): The password for the vendor.
            **extra_fields: Additional fields to be saved in the vendor model.

        Returns:
            Vendor: The created vendor object.
        """
        extra_fields.setdefault("is_vendor", True)
        return self.create_user(email, password, username, phone, **extra_fields)
