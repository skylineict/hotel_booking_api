""" This module contains the urls for the usersauth app. """
from django.urls import path
from .vendors import vendor_signup
from .views import (
    UserSignup,
    UserLogin,
    UserUpdate,
    ActivateAccount,
    ResendOTP,
    ListHotelBooking,
    ListApartmentBooking,
)

urlpatterns = [
    path("signup", UserSignup.as_view(), name="signup"),
    path("login", UserLogin.as_view(), name="login"),
    path("update", UserUpdate.as_view(), name="update"),
    path("activate", ActivateAccount.as_view(), name="activate"),
    path("resend-otp", ResendOTP.as_view(), name="resend-otp"),
    path("vendor-signup", vendor_signup, name="vendor-signup"),
    path("hotel-bookings", ListHotelBooking.as_view(), name="hotel-bookings"),
    path("apartment-bookings", ListApartmentBooking.as_view(), name="apartment-bookings"),
]
