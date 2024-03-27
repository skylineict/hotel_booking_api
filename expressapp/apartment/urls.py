""" This module contains the urls for the apartment app. """

from django.urls import path

from .views import (
    CreateApartment,
    RetrieveApartment,
    UpdateApartment,
    DeleteApartment,
    ListApartments,
    BookApartment,
    ListBookings,
)

urlpatterns = [
    path("create/", CreateApartment.as_view(), name="create apartment"),
    path("retrieve/", RetrieveApartment.as_view(), name="retrieve apartment"),
    path("update/", UpdateApartment.as_view(), name="update apartment"),
    path("delete/", DeleteApartment.as_view(), name="delete apartment"),
    path("list/", ListApartments.as_view(), name="list apartments"),
    path("book/", BookApartment.as_view(), name="book apartment"),
    path("bookings/", ListBookings.as_view(), name="list bookings"),
]
