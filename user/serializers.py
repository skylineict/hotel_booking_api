""" Serializers for the user app. """

from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializer(ModelSerializer):
    """Serializer for the User model."""

    class Meta:
        """Meta class for the UserSerializer."""

        model = User

        exclude = [
            "last_login",
            "verification_otp",
            "verification_otp_expiration",
            "reset_password_otp",
            "reset_password_otp_expiration",
        ]
        read_only_fields = [
            "id",
            "is_vendor",
            "email_verified",
            "phone_verified",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class UserUpdateSerializer(ModelSerializer):
    """Serializer for the UserUpdate model."""

    class Meta:
        """Meta class for the UserUpdateSerializer."""

        model = User
        fields = ["firstname", "lastname", "username", "gender"]
        extra_kwargs = {
            "firstname": {"required": False},
            "lastname": {"required": False},
            "username": {"required": False},
            "gender": {"required": False},
        }


class UserLoginSerializer(ModelSerializer):
    """Serializer for the UserLogin model."""

    class Meta:
        """Meta class for the UserLoginSerializer."""

        model = User
        fields = (
            "email",
            "password",
        )
        extra_kwargs = {
            "email": {"required": True, "validators": []},
            "password": {"required": True},
        }


class EmailVerificationSerializer(ModelSerializer):
    """Serializer for the EmailVerification."""

    class Meta:
        """Meta class for the EmailVerificationSerializer."""

        model = User
        fields = (
            "email",
            "verification_otp",
        )
        extra_kwargs = {
            "email": {"required": True, "validators": []},
            "verification_otp": {"required": True},
        }


class ResendOTPSerializer(ModelSerializer):
    """Serializer for the UserResendOTP model."""

    class Meta:
        """Meta class for the UserResendOTPSerializer."""

        model = User
        fields = ("email",)
        extra_kwargs = {
            "email": {"required": True, "validators": []},
        }
