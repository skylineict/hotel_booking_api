""" This module contains the views for the usersauth app. """
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apartment_booking.models import ApartmentBooking
from apartment_booking.serializers import ApartmentBookingSerializer
from hotel_booking.models import HotelBooking
from hotel_booking.serializers import HotelBookingSerializer

from .models import User
from .serializers import UserSerializer, UserSignupSerializer, UserActivationSerializer, ResendOTPSerializer, UserLoginSerializer
from .utils import generate_otp


class UserSignup(APIView):
    """ View for user signup."""
    serializer_class = UserSignupSerializer

    @swagger_auto_schema(
        request_body=UserSignupSerializer,
        responses={201: UserSerializer()},
    )
    def post(self, request):
        """Create a new user."""
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            otp = generate_otp()
            otp_expiry = timezone.now() + timezone.timedelta(minutes=30)
            serializer.validated_data["otp"] = otp
            serializer.validated_data["otp_expiry"] = otp_expiry
            serializer.save()

            send_mail(
                "JE Express Account Activation",
                f"Your OTP is {otp}. Use it to activate your account.",
                None,
                [serializer.validated_data["email"]],
                fail_silently=False,
            )
            serializer = UserSerializer(serializer.instance)

            return Response(
                {
                    "message": "User signup success!, OTP sent to your email.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        raise ValidationError(serializer.errors)


class UserLogin(APIView):
    """ API endpoint for user login. """
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={200: UserSerializer()},
    )
    def post(self, request):
        """ Handle user login. """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = User.objects.filter(email=email).first()

            if user is None:
                raise ValidationError({"message": "User does not exist!"})

            if not user.is_active:
                raise ValidationError({"message": "Account is not activated!"})

            authenticated_user = authenticate(email=email, password=password)

            if authenticated_user is not None:
                refresh = RefreshToken.for_user(authenticated_user)
                serializer = UserSerializer(authenticated_user)
                return Response(
                    {
                        "message": "Login successful!",
                        "data": serializer.data,
                        "access_token": str(refresh.access_token),
                        "refresh_token": str(refresh),
                    },
                    status=status.HTTP_200_OK,
                )
            raise ValidationError({"message": "Invalid credentials!"})
        raise ValidationError(serializer.errors)


class ActivateAccount(APIView):
    """ API endpoint for account activation. """
    serializer_class = UserActivationSerializer

    @swagger_auto_schema(
        request_body=UserActivationSerializer,
        responses={200: UserSerializer()},
    )
    def post(self, request):
        """Handle account activation."""
        serializer = UserActivationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp = serializer.validated_data["otp"]

            user = User.objects.filter(email=email).first()

            if user is None:
                raise ValidationError({"message": "User does not exist!"})

            if user.is_active:
                raise ValidationError({"message": "Account is already activated!"})

            if user.otp != otp:
                raise ValidationError({"message": "Invalid OTP!"})

            if user.otp_expiry < timezone.now():
                raise ValidationError({"message": "OTP has expired!"})

            user.is_active = True
            user.otp = None
            user.otp_expiry = None
            user.save()
            return Response(
                {"message": "Account activated successfully!"},
                status=status.HTTP_200_OK,
            )
        raise ValidationError(serializer.errors)


class ResendOTP(APIView):
    """ API endpoint for resending OTP. """
    serializer_class = ResendOTPSerializer

    @swagger_auto_schema(
        request_body=ResendOTPSerializer,
        responses={200: UserSerializer()},
    )
    def post(self, request):
        """ Handle resending OTP. """
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.filter(email=email).first()

            if user is None:
                raise ValidationError({"message": "User does not exist!"})

            otp = generate_otp()
            otp_expiry = timezone.now() + timezone.timedelta(minutes=30)
            user.otp = otp
            user.otp_expiry = otp_expiry
            user.save()

            send_mail(
                "JE Express Account Activation",
                f"Your OTP is {otp}. Use it to activate your account.",
                None,
                [user.email],
                fail_silently=False,
            )

            return Response(
                {"message": "OTP sent to your email!"},
                status=status.HTTP_200_OK,
            )
        raise ValidationError(serializer.errors)

    
class ListHotelBooking(APIView):
    """List all Hotel bookings by a user."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """List all Hotel bookings by a user."""
        bookings = HotelBooking.objects.filter(user=request.user.id)
        serializer = HotelBookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListApartmentBooking(APIView):
    """List all Apartment bookings by a user."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """ List all Apartment bookings by a user."""

        bookings = ApartmentBooking.objects.filter(user=request.user.id)
        serializer = ApartmentBookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
