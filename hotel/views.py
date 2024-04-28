""" This module contains the views for the user app. """

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema

from hotel.models import Hotel
from hotel_booking.models import HotelBooking
from .serializers import (
    HotelSerializer,
    UpdateHotelSerializer,
    HotelRoomSerializer,
    HotelBookingSerializer,
)
from hotel_booking.serializers import HotelBookingSerializer


class CreateHotel(APIView):
    """
    View to create a hotel in the system.

    - Requires token authentication.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HotelSerializer

    @swagger_auto_schema(
        request_body=HotelSerializer,
        responses={201: HotelSerializer, 400: "Bad Request"},
    )
    def post(self, request):
        """Create a new hotel."""
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() / m
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HotelView(APIView):
    """
    View to retrieve a hotel by its hotel_id.

    - Requires token authentication.
    - Requires hotel_id.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HotelSerializer

    def get(self, request, hotel_id):
        """Retrieve a hotel by its hotel_id."""
        try:
            hotel = Hotel.objects.get(hotel_id=hotel_id)
        except Hotel.DoesNotExist:
            return Response(
                {"message": "Hotel not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = HotelSerializer(hotel)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UpdateHotelSerializer,
        responses={201: HotelSerializer, 400: "Bad Request"},
    )
    def put(self, request, hotel_id):
        """Update a hotel."""
        try:
            hotel = Hotel.objects.get(hotel_id=hotel_id)
        except Hotel.DoesNotExist:
            return Response(
                {"message": "Hotel not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = UpdateHotelSerializer(hotel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, hotel_id):
        """Delete a hotel."""
        if not hotel_id:
            return Response(
                {"error": "hotel_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            hotel = Hotel.objects.get(hotel_id=hotel_id)
        except Hotel.DoesNotExist:
            return Response(
                {"message": "Hotel not found."}, status=status.HTTP_404_NOT_FOUND
            )
        hotel.delete()
        return Response({"message": "Hotel deleted."}, status=status.HTTP_200_OK)


class ListHotels(APIView):
    """
    View to list all hotels in the system.

    - Requires token authentication.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HotelSerializer

    def get(self, request):
        """List all hotels in the system."""
        filters = request.data

        if filters:
            # Key-value pairs not working
            hotels = Hotel.objects.filter(**filters)
        else:
            hotels = Hotel.objects.all()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeactivateHotel(APIView):
    """
    View to deactivate a hotel in the system.

    - Requires token authentication.
    - Requires hotel_id.
    """

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        """Deactivate a hotel."""
        hotel_id = request.query_params.get("hotel_id")
        if not hotel_id:
            return Response(
                {"error": "hotel_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            hotel = Hotel.objects.get(hotel_id=hotel_id)
        except Hotel.DoesNotExist:
            return Response(
                {"message": "Hotel not found."}, status=status.HTTP_404_NOT_FOUND
            )
        hotel.registration_status = False
        hotel.save()
        return Response({"message": "Hotel deactivated."}, status=status.HTTP_200_OK)


class ActivateHotel(APIView):
    """
    View to activate a hotel in the system.

    - Requires token authentication.
    - Requires hotel_id.
    """

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, hotel_id):
        """Activate a hotel."""
        try:
            hotel = Hotel.objects.get(hotel_id=hotel_id)
        except Hotel.DoesNotExist:
            return Response(
                {"message": "Hotel not found."}, status=status.HTTP_404_NOT_FOUND
            )
        hotel.registration_status = True
        hotel.save()
        return Response({"message": "Hotel activated."}, status=status.HTTP_200_OK)


class CreateRoom(APIView):
    """
    View to create a room in a hotel.

    - Requires token authentication.
    - Requires hotel_id.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HotelRoomSerializer

    @swagger_auto_schema(
        request_body=HotelRoomSerializer,
        responses={201: HotelRoomSerializer()},
    )
    def post(self, request, hotel_id):
        """Create a new room in a hotel."""
        try:
            hotel = Hotel.objects.get(hotel_id=hotel_id)
        except Hotel.DoesNotExist:
            return Response(
                {"error": "Hotel does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = HotelRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["hotel"] = hotel
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateRoom(APIView):
    """
    View to update a room in a hotel.

    - Requires token authentication.
    - Requires room_id.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HotelRoomSerializer

    def put(self, request):
        """Update a room in a hotel."""
        room_id = request.query_params.get("room_id")
        if not room_id:
            return Response(
                {"error": "room_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            room = HotelRoom.objects.get(room_id=room_id)
        except HotelRoom.DoesNotExist:
            return Response(
                {"message": "Room not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = HotelRoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteRoom(APIView):
    """
    View to delete a room in a hotel.

    - Requires token authentication.
    - Requires room_id.
    """

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        """Delete a room in a hotel."""
        room_id = request.query_params.get("room_id")
        if not room_id:
            return Response(
                {"error": "room_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            room = HotelRoom.objects.get(room_id=room_id)
        except HotelRoom.DoesNotExist:
            return Response(
                {"message": "Room not found."}, status=status.HTTP_404_NOT_FOUND
            )
        room.delete()
        return Response({"message": "Room deleted."}, status=status.HTTP_200_OK)


class ListRooms(APIView):
    """
    View to list all rooms in a hotel.

    - Requires token authentication.
    - Requires hotel_id.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HotelRoomSerializer

    def get(self, request, hotel_id):
        """List all rooms in a hotel."""
        try:
            hotel = Hotel.objects.get(hotel_id=hotel_id)
        except Hotel.DoesNotExist:
            return Response(
                {"message": "Hotel not found."}, status=status.HTTP_404_NOT_FOUND
            )
        rooms = hotel.rooms.all()
        serializer = HotelRoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookHotel(APIView):
    """
    View to book a hotel in the system.

    - Requires token authentication.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HotelBookingSerializer

    @swagger_auto_schema(
        request_body=HotelBookingSerializer,
        responses={201: HotelBookingSerializer()},
    )
    def post(self, request, hotel_id):
        """Book a hotel."""
        serializer = HotelBookingSerializer(data=request.data)
        if serializer.is_valid():
            hotel = Hotel.objects.get(hotel_id=request.data["hotel"])
            total_price = int(hotel.price) * int(request.data["guests"])
            serializer.validated_data["total_price"] = total_price

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelBooking(APIView):
    """
    View to cancel a booking in the system.

    - Requires token authentication.
    - Requires booking_id.
    """

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        """Cancel a booking."""
        booking_id = request.query_params.get("booking_id")
        if not booking_id:
            return Response(
                {"error": "booking_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            booking = HotelBooking.objects.get(booking_id=booking_id)
        except HotelBooking.DoesNotExist:
            return Response(
                {"message": "Booking not found."}, status=status.HTTP_404_NOT_FOUND
            )
        booking.delete()
        return Response({"message": "Booking cancelled."}, status=status.HTTP_200_OK)


class CheckoutBooking(APIView):
    """
    View to checkout a booking in the system.

    - Requires token authentication.
    - Requires booking_id.
    """

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        """Checkout a booking."""
        booking_id = request.query_params.get("booking_id")
        if not booking_id:
            return Response(
                {"error": "booking_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            booking = HotelBooking.objects.get(booking_id=booking_id)
        except HotelBooking.DoesNotExist:
            return Response(
                {"message": "Booking not found."}, status=status.HTTP_404_NOT_FOUND
            )
        booking.check_out = timezone.now()
        booking.save()
        return Response({"message": "Booking checked out."}, status=status.HTTP_200_OK)


class ListBookings(APIView):
    """
    View to list all bookings in the system.

    - Requires token authentication.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HotelBookingSerializer

    def get(self, request, hotel_id):
        """List all bookings in the system."""
        filters = request.data

        if filters:
            bookings = HotelBooking.objects.filter(
                **filters
            )  # Key-value pairs not working
        else:
            bookings = HotelBooking.objects.all()
        serializer = HotelBookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
