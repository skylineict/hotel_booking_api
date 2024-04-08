""" This module contains the urls for the hotel app. """

from django.urls import path
from .views import CheckoutBooking, CancelBooking

urlpatterns = [
    path("checkout/", CheckoutBooking.as_view(), name="checkout booking"),
    path("cancel/", CancelBooking.as_view(), name="cancel booking"),
]
