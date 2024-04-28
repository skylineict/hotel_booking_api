""" This module contains the urls for the user app. """

from django.urls import path
from .views import (
    UserSignup,
    UserLogin,
    EmailVerification,
    UserUpdate,
)

urlpatterns = [
    path("signup", UserSignup.as_view(), name="signup"),
    path("login", UserLogin.as_view(), name="login"),
    path("update", UserUpdate.as_view(), name="update"),
    path("verify-email", EmailVerification.as_view(), name="verify-email"),
    # path("activate", ActivateAccount.as_view(), name="activate"),
    # path("resend-otp", ResendOTP.as_view(), name="resend-otp"),
    # path("vendor-signup", vendor_signup, name="vendor-signup"),
    # path(
    #     "apartment-bookings",
    #     ListApartmentBooking.as_view(),
    #     name="apartment-bookings",
    # ),
]
