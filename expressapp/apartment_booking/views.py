""" This module contains the views for the apartment booking application. """

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions

from .models import ApartmentBooking

# from .models import Booking
from .serializers import CheckoutBookingSerializer


class CheckoutBooking(APIView):
    """
    View to checkout a booking in the system.

    - Requires token authentication.
    - Requires booking_id.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CheckoutBookingSerializer

    def post(self, request):
        """Checkout a booking."""
        booking_id = request.data.get("booking_id")
        try:
            booking = ApartmentBooking.objects.get(booking_id=booking_id)
        except ApartmentBooking.DoesNotExist:
            return Response(
                {"message": "Booking not found."}, status=status.HTTP_404_NOT_FOUND
            )
        booking.status = "completed"
        booking.save()
        return Response({"message": "Booking checked out."}, status=status.HTTP_200_OK)


class CancelBooking(APIView):
    """
    View to cancel a booking in the system.

    - Requires token authentication.
    - Requires booking_id.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CheckoutBookingSerializer

    def post(self, request):
        """Cancel a booking."""
        booking_id = request.data.get("booking_id")
        try:
            booking = ApartmentBooking.objects.get(booking_id=booking_id)
        except ApartmentBooking.DoesNotExist:
            return Response(
                {"message": "Booking not found."}, status=status.HTTP_404_NOT_FOUND
            )
        booking.status = "cancelled"
        booking.save()
        return Response({"message": "Booking cancelled."}, status=status.HTTP_200_OK)
