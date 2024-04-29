""" This module contains the urls for the user app. """

from django.urls import path
from .views import (
    UserSignup,
    UserLogin,
    UserUpdate,
    EmailVerification,
    ForgotPassword,
    ValidateResetOTP,
    ResetPasswordView,
    ResendOTP,
    SuspendUser,
    UnsuspendUser,
)

urlpatterns = [
    path("signup", UserSignup.as_view()),
    path("login", UserLogin.as_view()),
    path("update", UserUpdate.as_view()),
    path("verify-email", EmailVerification.as_view()),
    path("forgot-password/<str:email>", ForgotPassword.as_view()),
    path("validate-reset-otp", ValidateResetOTP.as_view()),
    path("reset-password", ResetPasswordView.as_view()),
    path("resend-otp", ResendOTP.as_view()),
    path("suspend", SuspendUser.as_view()),
    path("unsuspend", UnsuspendUser.as_view()),
    # path("resend-otp", ResendOTP.as_view(), name="resend-otp"),
    # path("vendor-signup", vendor_signup, name="vendor-signup"),
    # path(
    #     "apartment-bookings",
    #     ListApartmentBooking.as_view(),
    #     name="apartment-bookings",
    # ),
]
