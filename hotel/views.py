""" This module contains the views for the user app. """

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema

from hotel.models import Hotel
from .serializers import (
    HotelSerializer,
)


# class HotelList(APIView):
#     """List all hotels."""

#     permission_classes = [permissions.IsAuthenticated]

#     @swagger_auto_schema(
#         operation_summary="List all hotels.",
#         responses={201: HotelSerializer(many=True)},
#         tags=["hotel"],
#     )
#     def get(self, request):
#         """List all hotels."""
#         hotels = Hotel.objects.all()
#         hotel_serializer = HotelSerializer(hotels, many=True)
#         return CustomResponse(hotel_serializer.data, "List of all hotels", 200)


class CreateHotel(APIView):
    """
    View to create a hotel in the system.

    - Requires token authentication.
    """

    # permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=HotelSerializer,
        responses={201: HotelSerializer, 400: "Bad Request"},
    )
    def post(self, request):
        """Create a new hotel."""
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            hotel_data = {
                key: value
                for key, value in data.items()
                if key != "facilities"
            }
            hotel_data = {
                key: value
                for key, value in hotel_data.items()
                if key != "images"
            }
            hotel = Hotel(**hotel_data)
            hotel.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class HotelView(APIView):
#     """
#     View to retrieve a hotel by its hotel_id.

#     - Requires token authentication.
#     - Requires hotel_id.
#     """

#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = HotelSerializer

#     def get(self, request, hotel_id):
#         """Retrieve a hotel by its hotel_id."""
#         try:
#             hotel = Hotel.objects.get(hotel_id=hotel_id)
#         except Hotel.DoesNotExist:
#             return Response(
#                 {"message": "Hotel not found."}, status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = HotelSerializer(hotel)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         request_body=UpdateHotelSerializer,
#         responses={201: HotelSerializer, 400: "Bad Request"},
#     )
#     def put(self, request, hotel_id):
#         """Update a hotel."""
#         try:
#             hotel = Hotel.objects.get(hotel_id=hotel_id)
#         except Hotel.DoesNotExist:
#             return Response(
#                 {"message": "Hotel not found."}, status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = UpdateHotelSerializer(hotel, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, hotel_id):
#         """Delete a hotel."""
#         if not hotel_id:
#             return Response(
#                 {"error": "hotel_id is required"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         try:
#             hotel = Hotel.objects.get(hotel_id=hotel_id)
#         except Hotel.DoesNotExist:
#             return Response(
#                 {"message": "Hotel not found."}, status=status.HTTP_404_NOT_FOUND
#             )
#         hotel.delete()
#         return Response({"message": "Hotel deleted."}, status=status.HTTP_200_OK)


# class ListHotels(APIView):
#     """
#     View to list all hotels in the system.
#     """

#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = HotelSerializer

#     def get(self, request):
#         """List all hotels in the system."""
#         filters = request.data

#         if filters:
#             # Key-value pairs not working
#             hotels = Hotel.objects.filter(**filters)
#         else:
#             hotels = Hotel.objects.all()
#         serializer = HotelSerializer(hotels, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class DeactivateHotel(APIView):
#     """
#     View to deactivate a hotel in the system.

#     - Requires token authentication.
#     - Requires hotel_id.
#     """

#     permission_classes = [permissions.IsAuthenticated]

#     def put(self, request):
#         """Deactivate a hotel."""
#         hotel_id = request.query_params.get("hotel_id")
#         if not hotel_id:
#             return Response(
#                 {"error": "hotel_id is required"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         try:
#             hotel = Hotel.objects.get(hotel_id=hotel_id)
#         except Hotel.DoesNotExist:
#             return Response(
#                 {"message": "Hotel not found."}, status=status.HTTP_404_NOT_FOUND
#             )
#         hotel.registration_status = False
#         hotel.save()
#         return Response({"message": "Hotel deactivated."}, status=status.HTTP_200_OK)


# class ActivateHotel(APIView):
#     """
#     View to activate a hotel in the system.

#     - Requires token authentication.
#     - Requires hotel_id.
#     """

#     permission_classes = [permissions.IsAuthenticated]

#     def put(self, request, hotel_id):
#         """Activate a hotel."""
#         try:
#             hotel = Hotel.objects.get(hotel_id=hotel_id)
#         except Hotel.DoesNotExist:
#             return Response(
#                 {"message": "Hotel not found."}, status=status.HTTP_404_NOT_FOUND
#             )
#         hotel.registration_status = True
#         hotel.save()
#         return Response({"message": "Hotel activated."}, status=status.HTTP_200_OK)


# class CreateRoom(APIView):
#     """
#     View to create a room in a hotel.

#     - Requires token authentication.
#     - Requires hotel_id.
#     """

#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = HotelRoomSerializer

#     @swagger_auto_schema(
#         request_body=HotelRoomSerializer,
#         responses={201: HotelRoomSerializer()},
#     )
#     def post(self, request, hotel_id):
#         """Create a new room in a hotel."""
#         try:
#             hotel = Hotel.objects.get(hotel_id=hotel_id)
#         except Hotel.DoesNotExist:
#             return Response(
#                 {"error": "Hotel does not exist"}, status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = HotelRoomSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.validated_data["hotel"] = hotel
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UpdateRoom(APIView):
#     """
#     View to update a room in a hotel.

#     - Requires token authentication.
#     - Requires room_id.
#     """

#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = HotelRoomSerializer

#     def put(self, request):
#         """Update a room in a hotel."""
#         room_id = request.query_params.get("room_id")
#         if not room_id:
#             return Response(
#                 {"error": "room_id is required"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         try:
#             room = HotelRoom.objects.get(room_id=room_id)
#         except HotelRoom.DoesNotExist:
#             return Response(
#                 {"message": "Room not found."}, status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = HotelRoomSerializer(room, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class DeleteRoom(APIView):
#     """
#     View to delete a room in a hotel.

#     - Requires token authentication.
#     - Requires room_id.
#     """

#     permission_classes = [permissions.IsAuthenticated]

#     def delete(self, request):
#         """Delete a room in a hotel."""
#         room_id = request.query_params.get("room_id")
#         if not room_id:
#             return Response(
#                 {"error": "room_id is required"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         try:
#             room = HotelRoom.objects.get(room_id=room_id)
#         except HotelRoom.DoesNotExist:
#             return Response(
#                 {"message": "Room not found."}, status=status.HTTP_404_NOT_FOUND
#             )
#         room.delete()
#         return Response({"message": "Room deleted."}, status=status.HTTP_200_OK)


# class ListRooms(APIView):
#     """
#     View to list all rooms in a hotel.

#     - Requires token authentication.
#     - Requires hotel_id.
#     """

#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = HotelRoomSerializer

#     def get(self, request, hotel_id):
#         """List all rooms in a hotel."""
#         try:
#             hotel = Hotel.objects.get(hotel_id=hotel_id)
#         except Hotel.DoesNotExist:
#             return Response(
#                 {"message": "Hotel not found."}, status=status.HTTP_404_NOT_FOUND
#             )
#         rooms = hotel.rooms.all()
#         serializer = HotelRoomSerializer(rooms, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
