""" This module contains the views for the usersauth app. """

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions

from hotel.models import Hotel
from hotel_booking.models import HotelBooking
from .serializers import HotelSerializer, UpdateHotelSerializer
from hotel_booking.serializers import HotelBookingSerializer


class CreateHotel(APIView):
    """
    View to create a hotel in the system.

    - Requires token authentication.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HotelSerializer

    def post(self, request):
        """Create a new hotel."""
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveHotel(APIView):
    """
    View to retrieve a hotel by its hotel_id.

    - Requires token authentication.
    - Requires hotel_id.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HotelSerializer

    def get(self, request):
        """Retrieve a hotel by its hotel_id."""
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
        serializer = HotelSerializer(hotel)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateHotel(APIView):
    """
    View to update a hotel in the system.

    - Requires token authentication.
    - Requires hotel_id.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HotelSerializer

    def put(self, request):
        """Update a hotel."""
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
        serializer = UpdateHotelSerializer(hotel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteHotel(APIView):
    """
    View to delete a hotel in the system.

    - Requires token authentication.
    - Requires hotel_id.
    """

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        """Delete a hotel."""
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
            hotels = Hotel.objects.filter(**filters)  # Key-value pairs not working
        else:
            hotels = Hotel.objects.all()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookHotel(APIView):
    """
    View to book a hotel in the system.

    - Requires token authentication.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HotelBookingSerializer

    def post(self, request):
        """Book a hotel."""
        serializer = HotelBookingSerializer(data=request.data)
        if serializer.is_valid():
            hotel = Hotel.objects.get(hotel_id=request.data["hotel"])
            total_price = int(hotel.price) * int(request.data["guests"])
            serializer.validated_data["total_price"] = total_price

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListBookings(APIView):
    """
    View to list all bookings in the system.

    - Requires token authentication.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HotelBookingSerializer

    def get(self, request):
        """List all bookings in the system."""
        filters = request.data

        if filters:
            bookings = HotelBooking.objects.filter(**filters)  # Key-value pairs not working
        else:
            bookings = HotelBooking.objects.all()
        serializer = HotelBookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
