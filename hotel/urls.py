""" This module contains the urls for the hotel app. """

from django.urls import path
from .views import (
    CreateHotel,
    HotelView,
    ListHotels,
    DeactivateHotel,
    ActivateHotel,
    CreateRoom,
    UpdateRoom,
    DeleteRoom,
    ListRooms,
)

urlpatterns = [
    path("", ListHotels.as_view(), name="list hotels"),
    path("create", CreateHotel.as_view(), name="create hotel"),
    path("<str:hotel_id>", HotelView.as_view(), name="delete hotel"),
    path(
        "<str:hotel_id>/deactivate", DeactivateHotel.as_view(), name="deactivate hotel"
    ),
    path("<str:hotel_id>/activate", ActivateHotel.as_view(), name="activate hotel"),
    path("<str:hotel_id>/room/create", CreateRoom.as_view(), name="create room"),
    path("<str:hotel_id>/room/<str:room_id>", UpdateRoom.as_view(), name= "update room"),
    path("<str:hotel_id>/room/<str:room_id>", DeleteRoom.as_view(), name="delete room"),
    path("<str:hotel_id>/rooms", ListRooms.as_view(), name="list rooms"),
]
