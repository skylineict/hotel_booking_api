""" This module contains the urls for the user app. """

from django.urls import path
from .views import (
    UserView,
    UserSignup,
    VendorSignup,
    UserLogin,
    UserUpdate,
    EmailVerification,
    ForgotPassword,
    ValidateResetOTP,
    ResetPasswordView,
    ResendOTP,
    ActivateUser,
    DeactivateUser,
)

urlpatterns = [
    path("signup", UserSignup.as_view()),
    path("vendor-signup", VendorSignup.as_view()),
    path("login", UserLogin.as_view()),
    path("update", UserUpdate.as_view()),
    path("verify-email", EmailVerification.as_view()),
    path("forgot-password/<str:email>", ForgotPassword.as_view()),
    path("validate-reset-otp", ValidateResetOTP.as_view()),
    path("reset-password", ResetPasswordView.as_view()),
    path("resend-otp", ResendOTP.as_view()),
    path("<str:user_id>/suspend", ActivateUser.as_view()),
    path("<str:user_id>/unsuspend", DeactivateUser.as_view()),
    path("<str:user_id>", UserView.as_view()),
    # path("resend-otp", ResendOTP.as_view(), name="resend-otp"),
    # path("vendor-signup", vendor_signup, name="vendor-signup"),
    # path(
    #     "apartment-bookings",
    #     ListApartmentBooking.as_view(),
    #     name="apartment-bookings",
    # ),
]
