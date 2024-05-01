""" This module contains the views for the Image. """

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    ImageSerializer,
)


class ImageUploadView(APIView):
    """View for uploading images to the system."""

    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = ImageSerializer

    @swagger_auto_schema(
        operation_description="Upload an image",
        request_body=ImageSerializer,
        responses={200: ImageSerializer},
    )
    def post(self, request):
        """Upload an image to the system."""
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
