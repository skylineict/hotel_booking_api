""" Serializers for the hotel app. """

from rest_framework.serializers import (
    ModelSerializer,
    ManyRelatedField,
    URLField,
    BooleanField,
)
from .models import (
    Hotel,
    # HotelRoom,
    # HotelBooking,
    # HotelReview,
    Facility,
    HotelFacility,
)


class FacilitySerializer(ModelSerializer):
    """Serializer for the Facility model."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for facility in Facility.objects.all():
            self.fields[facility.id] = BooleanField(required=True)

    class Meta:
        """Meta class for defining metadata options for the Facility model."""

        model = Facility
        fields = []


class HotelSerializer(ModelSerializer):
    """Serializer for the Hotel model."""

    facilities = FacilitySerializer()
    images = ManyRelatedField(URLField())

    class Meta:
        """Meta class for defining metadata options for the Hotel model."""

        model = Hotel
        fields = "__all__"
        read_only_fields = (
            "hotel_id",
            "is_active",
            "owner",
            "date_registered",
            "date_updated",
        )

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        hotel = Hotel.objects.create(**validated_data)
        
        facilities_data = validated_data.pop("facilities")
        for facility_id, is_available in facilities_data.items():
            facility = Facility.objects.get(id=facility_id)
            hotel_facility = HotelFacility(
                hotel=hotel,
                facility=facility,
                is_available=is_available,
            )
            hotel_facility.save()
        return hotel


# class UpdateHotelSerializer(HotelSerializer):
#     """Serializer for updating a hotel in the system."""

#     class Meta(HotelSerializer.Meta):
#         """Meta class for defining metadata options for the Hotel model."""

#         extra_kwargs = {
#             "name": {"required": False},
#             "description": {"required": False},
#             "featured_image": {"required": False},
#             "facilities": {"required": False},
#             "images": {"required": False},
#             "address": {"required": False},
#             "city": {"required": False},
#             "state": {"required": False},
#             "country": {"required": False},
#             "registration_number": {"required": False},
#             "owner": {"required": False},
#         }

#         read_only_fields = (
#             "hotel_id",
#             "owner",
#             "registration_status",
#             "date_registered",
#             "date_updated",
#         )


# class HotelRoomSerializer(ModelSerializer):
#     """Serializer for the HotelRoom model."""

#     class Meta:
#         """Meta class for defining metadata options for the HotelRoom model."""

#         model = HotelRoom
#         fields = "__all__"
#         read_only_fields = ("room_id", "date_created", "date_updated", "hotel")
#         extra_kwargs = {"images": {"required": False}}

#     def create(self, validated_data):
#         room = HotelRoom.objects.create(**validated_data)
#         return room


# class UpdateHotelRoomSerializer(HotelRoomSerializer):
#     """Serializer for updating a hotel room in the system."""

#     class Meta(HotelRoomSerializer.Meta):
#         """Meta class for defining metadata options for the HotelRoom model."""

#         extra_kwargs = {
#             "room_type": {"required": False},
#             "room_number": {"required": False},
#             "description": {"required": False},
#             "price": {"required": False},
#             "images": {"required": False},
#         }


# class HotelBookingSerializer(ModelSerializer):
#     """Serializer for the HotelBooking model."""

#     class Meta:
#         """Meta class for defining metadata options for the HotelBooking model."""

#         model = HotelBooking
#         fields = "__all__"
#         read_only_fields = ("booking_id", "date_booked", "date_updated")
#         extra_kwargs = {"rooms": {"required": False}}

#     def create(self, validated_data):
#         booking = HotelBooking.objects.create(**validated_data)
#         return booking


# class HotelReviewSerializer(ModelSerializer):
#     """Serializer for the HotelReview model."""

#     class Meta:
#         """Meta class for defining metadata options for the HotelReview model."""

#         model = HotelReview
#         fields = "__all__"
#         read_only_fields = ("review_id", "date_reviewed")
#         extra_kwargs = {"rating": {"required": False}}
