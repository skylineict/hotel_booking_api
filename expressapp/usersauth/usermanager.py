""" This module contains the custom user manager for the user model. """

from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUsermanager(BaseUserManager):
    """
    Custom user manager for creating and managing user accounts.
    """

    def create_user(
        self, email, password, username=None, phone=None, **extra_fields
    ):
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
        user = self.model(
            email=email, username=username, phone=phone, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, username=None, phone=None, password=None, **extra_fields
    ):
        """
        Creates a new superuser with the email, username, phone, and password.

        Args:
            email (str): The email address of the superuser.
            username (str, optional): The username of the superuser.
            phone (str, optional): The phone number of the superuser.
            password (str, optional): The password for the superuser.
            **extra_fields: Additional fields to be saved in the user model.

        Returns:
            User: The created superuser object.
        """
        user = self.create_user(
            email=email,
            username=username,
            phone=phone,
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user
