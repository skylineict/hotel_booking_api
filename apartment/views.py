""" This module contains the views for the Apartment model in the system. """

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions

from .models import Apartment
from apartment_booking.models import ApartmentBooking
from .serializers import ApartmentSerializer, UpdateApartmentSerializer
from apartment_booking.serializers import ApartmentBookingSerializer


class CreateApartment(APIView):
    """
    View to create an apartment in the system.

    - Requires token authentication.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApartmentSerializer

    def post(self, request):
        """Create an apartment."""
        serializer = ApartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(agent=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveApartment(APIView):
    """
    View to retrieve an apartment by its apartment_id.

    - Requires token authentication.
    - Requires apartment_id.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApartmentSerializer

    def get(self, request):
        """Retrieve an apartment by its apartment_id."""
        apartment_id = request.query_params.get("apartment_id")
        if not apartment_id:
            return Response(
                {"error": "apartment_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            apartment = Apartment.objects.get(apartment_id=apartment_id)
        except Apartment.DoesNotExist:
            return Response(
                {"message": "Apartment not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ApartmentSerializer(apartment)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateApartment(APIView):
    """
    View to update an apartment in the system.

    - Requires token authentication.
    - Requires apartment_id.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateApartmentSerializer

    def put(self, request):
        """Update an apartment."""
        apartment_id = request.query_params.get("apartment_id")
        if not apartment_id:
            return Response(
                {"error": "apartment_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            apartment = Apartment.objects.get(apartment_id=apartment_id)
        except Apartment.DoesNotExist:
            return Response(
                {"message": "Apartment not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = UpdateApartmentSerializer(apartment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteApartment(APIView):
    """
    View to delete an apartment in the system.

    - Requires token authentication.
    - Requires apartment_id.
    """

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        """Delete an apartment."""
        apartment_id = request.query_params.get("apartment_id")
        if not apartment_id:
            return Response(
                {"error": "apartment_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            apartment = Apartment.objects.get(apartment_id=apartment_id)
        except Apartment.DoesNotExist:
            return Response(
                {"message": "Apartment not found."}, status=status.HTTP_404_NOT_FOUND
            )
        apartment.delete()
        return Response({"message": "Apartment deleted."}, status=status.HTTP_200_OK)


class ListApartments(APIView):
    """
    View to list all apartments in the system.

    - Requires token authentication.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApartmentSerializer

    def get(self, request):
        """List all apartments in the system."""
        filters = request.data

        if filters:
            apartments = Apartment.objects.filter(
                **filters
            )  # Key-value pairs not working
        else:
            apartments = Apartment.objects.all()
        serializer = ApartmentSerializer(apartments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookApartment(APIView):
    """
    View to book an apartment in the system.

    - Requires token authentication.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApartmentBookingSerializer

    def post(self, request):
        """Book an apartment."""
        serializer = ApartmentBookingSerializer(data=request.data)
        if serializer.is_valid():
            apartment = Apartment.objects.get(apartment_id=request.data["apartment"])
            total_price = int(apartment.price) * int(request.data["guests"])
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
    serializer_class = ApartmentBookingSerializer

    def get(self, request):
        """List all bookings in the system."""
        filters = request.data

        if filters:
            bookings = ApartmentBooking.objects.filter(
                **filters
            )  # Key-value pairs not working
        else:
            bookings = ApartmentBooking.objects.all()
        serializer = ApartmentBookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
