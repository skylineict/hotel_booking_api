""" This module contains the views for the usersauth app. """

import datetime
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .serializers import UserSerializer
from .utils import generate_otp
from django.urls import path


@api_view(("POST",))
@renderer_classes((JSONRenderer,))
def vendor_signup(request):
    """
    API endpoint for user signup.

    Args:
        request (Request): The request object.

    Returns:
        Response: The response object.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        otp = generate_otp()
        otp_expiry = datetime.datetime.now() + datetime.timedelta(minutes=5)
        serializer.validated_data["otp"] = otp
        serializer.validated_data["otp_expiry"] = otp_expiry
        serializer.validated_data["is_vendor"] = True
        send_mail(
            "JE Express Account Activation",
            f"Your OTP is {otp}. Use it to activate your account.",
            None,
            request.data["email"],
            fail_silently=False,
        )
        serializer.save()
        return Response(
            {
                "message": "User signup success!, OTP sent to your email.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {"message": "User signup failed!", "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )
