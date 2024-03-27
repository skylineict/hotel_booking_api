""" Serializers for the hotel app. """

from rest_framework.serializers import ModelSerializer
from .models import Hotel


class HotelSerializer(ModelSerializer):
    """Serializer for the Hotel model."""

    class Meta:
        """Meta class for defining metadata options for the Hotel model."""

        model = Hotel
        fields = "__all__"
        read_only_fields = ("hotel_id", "date_registered", "date_updated")
        extra_kwargs = {"images": {"required": False}}

    def create(self, validated_data):
        hotel = Hotel.objects.create(**validated_data)
        return hotel


class UpdateHotelSerializer(HotelSerializer):
    """Serializer for updating a hotel in the system."""

    class Meta(HotelSerializer.Meta):
        """Meta class for defining metadata options for the Hotel model."""

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
            "max_guests": {"required": False},
            "rooms": {"required": False},
            "price": {"required": False},
        }
