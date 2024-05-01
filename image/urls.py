""" This module contains the urls for the hotel app. """

from django.urls import path
from .views import ImageUploadView

urlpatterns = [path("upload", ImageUploadView.as_view())]
