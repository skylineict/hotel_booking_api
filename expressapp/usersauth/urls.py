from django.urls import path
from .views import (
    user_signup,
    user_login,
    activate_account,
    resend_otp,
)

urlpatterns = [
    path("signup/", user_signup, name="signup"),
    path("login/", user_login, name="login"),
    path("activate/", activate_account, name="activate"),
    path("resend-otp/", resend_otp, name="resend-otp"),
]
