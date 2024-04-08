from rest_framework.serializers import ModelSerializer
from .models import ApartmentBooking

""" Serializers for the booking app. """


class ApartmentBookingSerializer(ModelSerializer):
    """Serializer for the ApartmentBooking model."""

    class Meta:
        """Meta class for defining metadata options for the ApartmentBooking model."""

        model = ApartmentBooking
        fields = "__all__"
        read_only_fields = (
            "booking_id",
            "total_price",
            "status",
            "date_booked",
            "date_updated",
        )

    def create(self, validated_data):
        apartment_booking = ApartmentBooking.objects.create(**validated_data)
        return apartment_booking


class CheckoutBookingSerializer(ApartmentBookingSerializer):
    """Serializer for the CheckoutBooking model."""

    class Meta:
        """Meta class for defining metadata options for the CheckoutBooking model."""

        model = ApartmentBooking
        fields = ["booking_id"]
        extra_kwargs = {"booking_id": {"required": True, "read_only": False}}
