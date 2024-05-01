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
from image import urls as image_urls
from hotel import urls as hotel_urls
from user import urls as user_urls
from user.views import UserList


urlpatterns = [
    path("users", UserList.as_view()),
    path("user/", include(user_urls)),
    path("image/", include(image_urls)),
    path("hotel/", include(hotel_urls)),
    path("swagger", SchemaView.with_ui("swagger"), name="swagger-ui"),
    path("redoc", SchemaView.with_ui("redoc")),
    re_path(r"^$", lambda request: redirect("swagger-ui")),
]
