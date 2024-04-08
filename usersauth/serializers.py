""" Serializers for the usersauth app. """
from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializer(ModelSerializer):
    """ Serializer for the User model. """
    class Meta:
        """ Meta class for the UserSerializer."""
        model = User
        fields = (
            "id",
            "firstname",
            "lastname",
            "email",
            "username",
            "phone",
            "password",
            "date_joined",
        )
        read_only_fields = ("id", "date_joined")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }


class UserUpdateSerializer(ModelSerializer):
    """ Serializer for the UserUpdate model. """
    class Meta:
        """ Meta class for the UserUpdateSerializer."""
        model = User
        fields = (
            "id",
            "firstname",
            "lastname",
            "email",
            "phone",
            "username",
        )
        extra_kwargs = {
            "id": {"required": True},
            "email": {"required": True},
        }
        extra_fields = {
            "id": {"required": True},
        }


class UserSignupSerializer(ModelSerializer):
    """ Serializer for the UserSignup model. """
    class Meta:
        """ Meta class for the UserSignupSerializer."""
        model = User
        fields = (
            "email",
            "phone",
            "password",
        )
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(ModelSerializer):
    """ Serializer for the UserLogin model. """
    class Meta:
        """ Meta class for the UserLoginSerializer."""
        model = User
        fields = (
            "email",
            "password",
        )
        extra_kwargs = {
            "email": {"required": True, "validators": []},
            "password": {"required": True},
        }


class UserActivationSerializer(ModelSerializer):
    """ Serializer for the UserActivation model. """
    class Meta:
        """ Meta class for the UserActivationSerializer."""
        model = User
        fields = (
            "email",
            "otp",
        )
        extra_kwargs = {
            "email": {"required": True, "validators": []},
            "otp": {"required": True},
        }


class ResendOTPSerializer(ModelSerializer):
    """ Serializer for the UserResendOTP model. """
    class Meta:
        """ Meta class for the UserResendOTPSerializer."""
        model = User
        fields = (
            "email",
        )
        extra_kwargs = {
            "email": {"required": True, "validators": []},
        }
