"""
URL configuration for expressapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.shortcuts import redirect
from django.urls import include, path, re_path

from expressapp.swagger import SchemaView
from apartment import urls as apartment_urls
from apartment_booking import urls as apartment_booking_urls
from hotel import urls as hotel_urls
from hotel_booking import urls as hotel_booking_urls
from user import urls as userauth_urls
from user.views import UserView, UserList


urlpatterns = [
    path("users", UserList.as_view(), name="user-list"),
    path("users/<str:user_id>", UserView.as_view(), name="user-list"),
    path("user/", include(userauth_urls), name="User Authentication"),
    path("hotel/", include(hotel_urls)),
    path("apartment/", include(apartment_urls)),
    path("hotel-booking/", include(hotel_booking_urls)),
    path("apartment-booking/", include(apartment_booking_urls)),
    path("swagger/", SchemaView.with_ui("swagger"), name="swagger-ui"),
    path("redoc/", SchemaView.with_ui("redoc"), name="redoc"),
    re_path(r"^$", lambda request: redirect("swagger-ui")),
]
