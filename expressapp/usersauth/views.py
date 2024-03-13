""" This module contains the views for the usersauth app. """

import datetime
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .serializers import CustomUserSerializer
from .models import CustomUser
from .utils import generate_otp


@api_view(("POST",))
@renderer_classes((JSONRenderer,))
def user_signup(request):
    """
    API endpoint for user signup.

    Args:
        request (Request): The request object.

    Returns:
        Response: The response object.
    """
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        otp = generate_otp()
        otp_expiry = datetime.datetime.now() + datetime.timedelta(minutes=30)
        serializer.validated_data["otp"] = otp
        serializer.validated_data["otp_expiry"] = otp_expiry
        send_mail(
            "JE Express Account Activation",
            "Your OTP is 123345. Use it to activate your account.",
            None,
            ["destinedcodes@gmail.com"],
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

@api_view(("POST",))
@renderer_classes((JSONRenderer,))
def activate_account(request):
    """API endpoint for account activation."""
    email = request.data.get("email")
    otp = request.data.get("otp")

    if not email or not otp:
        missing_fields = []
        if not email:
            missing_fields.append("email")
        if not otp:
            missing_fields.append("otp")
        return Response(
            {"message": f"Missing fields: {', '.join(missing_fields)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = CustomUser.objects.filter(email=email).first()

    if user is None:
        return Response(
            {"message": "User does not exist!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if user.otp != otp:
        return Response(
            {"message": "Invalid OTP!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if user.otp_expiry < datetime.datetime.now():
        return Response(
            {"message": "OTP has expired!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.is_active = True
    user.save()
    return Response(
        {"message": "Account activation success!"},
        status=status.HTTP_200_OK,
    )

@api_view(("POST",))
@renderer_classes((JSONRenderer,))
def resend_otp(request):
    """API endpoint for resending OTP."""
    email = request.data.get("email")

    if not email:
        return Response(
            {"message": "Missing email field!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = CustomUser.objects.filter(email=email).first()

    if user is None:
        return Response(
            {"message": "User does not exist!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    otp = generate_otp()
    otp_expiry = datetime.datetime.now() + datetime.timedelta(minutes=30)
    user.otp = otp
    user.otp_expiry = otp_expiry
    send_mail(
        "JE Express Account Activation",
        f"Your OTP is {otp}. Use it to activate your account.",
        None,
        [email],
        fail_silently=False,
    )

    user.save()
    return Response(
        {"message": "OTP sent to your email!"},
        status=status.HTTP_200_OK,
    )

@api_view(("POST",))
@renderer_classes((JSONRenderer,))
def user_login(request):
    """API endpoint for user login."""
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        missing_fields = []
        if not email:
            missing_fields.append("email")
        if not password:
            missing_fields.append("password")
        return Response(
            {"message": f"Missing fields: {', '.join(missing_fields)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = CustomUser.objects.filter(email=email).first()

    if user is None:
        return Response(
            {"message": "User does not exist!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    authenticated_user = authenticate(email=email, password=password)

    if authenticated_user is not None:
        # check if the user is active
        if not authenticated_user.is_active:
            return Response(
                {"message": "Account is not activated!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        login(request, authenticated_user)
        return Response(
            {"message": "Login success!"},
            status=status.HTTP_200_OK,
        )
    return Response(
        {"message": "Invalid credentials!"},
        status=status.HTTP_400_BAD_REQUEST,
    )