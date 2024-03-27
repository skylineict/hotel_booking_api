""" This module contains the urls for the hotel app. """

from django.urls import path
from .views import (
    CreateHotel,
    RetrieveHotel,
    UpdateHotel,
    DeleteHotel,
    ListHotels,
    BookHotel,
    ListBookings,
)

urlpatterns = [
    path("create/", CreateHotel.as_view(), name="create hotel"),
    path("retrieve/", RetrieveHotel.as_view(), name="retrieve hotel"),
    path("update/", UpdateHotel.as_view(), name="update hotel"),
    path("delete/", DeleteHotel.as_view(), name="delete hotel"),
    path("list/", ListHotels.as_view(), name="list hotels"),
    path("book/", BookHotel.as_view(), name="book hotel"),
    path("bookings/", ListBookings.as_view(), name="list bookings"),
]
