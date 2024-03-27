""" Serializers for the booking app. """

from rest_framework.serializers import ModelSerializer
from .models import HotelBooking


class HotelBookingSerializer(ModelSerializer):
    """Serializer for the HotelBooking model."""

    class Meta:
        """Meta class for defining metadata options for the HotelBooking model."""

        model = HotelBooking
        fields = "__all__"
        read_only_fields = (
            "booking_id",
            "total_price",
            "status",
            "date_booked",
            "date_updated",
        )

    def create(self, validated_data):
        hotel_booking = HotelBooking.objects.create(**validated_data)
        return hotel_booking


class CheckoutBookingSerializer(HotelBookingSerializer):
    """Serializer for the CheckoutBooking model."""

    class Meta:
        """Meta class for defining metadata options for the CheckoutBooking model."""

        model = HotelBooking
        fields = ["booking_id"]
        extra_kwargs = {"booking_id": {"required": True, "read_only": False}}
