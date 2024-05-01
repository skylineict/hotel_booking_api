""" Serializers for the hotel app. """

from cloudinary.forms import CloudinaryFileField
from rest_framework.serializers import ModelSerializer

from .models import Image


class ImageSerializer(ModelSerializer):
    """Serializer for the Photo model."""

    image = CloudinaryFileField()

    class Meta:
        """Meta class for defining metadata options for the serializer."""

        model = Image
        fields = ["image"]
        read_only_fields = ["url"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].options = {"tags": "new_image", "format": "png"}
