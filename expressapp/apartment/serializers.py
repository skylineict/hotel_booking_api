""" Serializers for the apartment app. """

from rest_framework.serializers import ModelSerializer
from .models import Apartment


class ApartmentSerializer(ModelSerializer):
    """Serializer for the Apartment model."""

    class Meta:
        """Meta class for defining metadata options for the Apartment model."""

        model = Apartment
        fields = "__all__"
        read_only_fields = ("apartment_id", "date_registered", "date_updated")
        extra_kwargs = {"images": {"required": False}}

    def create(self, validated_data):
        hotel = Apartment.objects.create(**validated_data)
        return hotel


class UpdateApartmentSerializer(ApartmentSerializer):
    """Serializer for updating a apartment in the system."""

    class Meta(ApartmentSerializer.Meta):
        """Meta class for defining metadata options for the Apartment model."""

        extra_kwargs = {
            "name": {"required": False},
            "description": {"required": False},
            "featured_image": {"required": False},
            "images": {"required": False},
            "address": {"required": False},
            "city": {"required": False},
            "state": {"required": False},
            "country": {"required": False},
            "registration_number": {"required": False},
            "rooms": {"required": False},
            "price": {"required": False},
        }
