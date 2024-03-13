from rest_framework.serializers import ModelSerializer
from .models import CustomUser


class CustomUserSerializer(ModelSerializer):
    """ Serializer for the CustomUser model. """
    class Meta:
        """ Meta class for the CustomUserSerializer."""
        model = CustomUser
        fields = (
            "id",
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

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
