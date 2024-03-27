from django.urls import path
from .vendors import vendor_signup
from .views import (
    user_signup,
    user_login,
    activate_account,
    resend_otp,
    ListHotelBooking,
    ListApartmentBooking,
)

urlpatterns = [
    path("signup/", user_signup, name="signup"),
    path("login/", user_login, name="login"),
    path("activate/", activate_account, name="activate"),
    path("resend-otp/", resend_otp, name="resend-otp"),
    path("vendor-signup", vendor_signup, name="vendor-signup"),
    path("hotel-bookings/", ListHotelBooking.as_view(), name="hotel-bookings"),
    path("apartment-bookings/", ListApartmentBooking.as_view(), name="apartment-bookings"),
]
