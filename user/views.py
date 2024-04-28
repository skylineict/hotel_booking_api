""" This module contains the views for the user app. """

from django.contrib.auth import authenticate
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apartment_booking.models import ApartmentBooking
from apartment_booking.serializers import ApartmentBookingSerializer
from hotel_booking.models import HotelBooking
from hotel_booking.serializers import HotelBookingSerializer
from expressapp.utils import CustomResponse, CustomException

from .models import User
from .serializers import (
    UserSerializer,
    UserActivationSerializer,
    ResendOTPSerializer,
    UserLoginSerializer,
    UserUpdateSerializer,
)


class UserSignup(APIView):
    """Create a new user account."""

    @swagger_auto_schema(
        operation_summary="Create a new user account.",
        request_body=UserSerializer,
        responses={201: UserSerializer()},
    )
    def post(self, request):
        """Create a new user account."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            user.generate_verification_otp()

            return Response(
                {
                    "status": "success",
                    "message": "Verification OTP sent to your email.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return CustomException(serializer.errors, 400)


class UserList(APIView):
    """List all users."""

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List all users.",
        responses={201: UserSerializer(many=True)},
        tags=["user"],
    )
    def get(self, request):
        """List all users."""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return CustomResponse(serializer.data, "List of all users", 200)


class UserView(APIView):
    """Retrieve a user."""

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve a user.",
        responses={201: UserSerializer()},
        tags=["user"],
    )
    def get(self, request, user_id: str):
        """Retrieve a user."""
        user = User.objects.filter(id=user_id).first()
        if not user:
            return CustomException(
                f"{user_id or request.user.id} not found", 404
            )
        serializer = UserSerializer(user)
        return CustomResponse(
            serializer.data, "User retrieved successfully", 200
        )


class UserUpdate(APIView):
    """Update a user."""

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Update a user.",
        request_body=UserUpdateSerializer,
        responses={200: UserSerializer()},
    )
    def put(self, request):
        """Update a user."""
        serializer = UserUpdateSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer = UserSerializer(serializer)

            return Response(
                {"message": "User updated", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return CustomException(serializer.errors, 400)


class UserLogin(APIView):
    """Authenticate a user."""

    @swagger_auto_schema(
        operation_summary="Authenticate a user.",
        request_body=UserLoginSerializer,
        responses={200: UserSerializer()},
    )
    def post(self, request):
        """Handle user login."""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(email=email, password=password)

            if not user:
                return CustomException("Invalid email or password", 401)

            if not user.email_verified:
                return CustomException("Email not verified", 401)

            # access_token = RefreshToken.for_user(user).access_token
            return CustomResponse(user, "Logged in successfully", 200)
        return CustomException(serializer.errors, 400)


class ResetPassword(APIView):
    """API endpoint for resetting password."""

    serializer_class = ResendOTPSerializer

    @swagger_auto_schema(
        request_body=ResendOTPSerializer,
        responses={200: UserSerializer()},
    )
    def post(self, request):
        """Handle resetting password."""
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.filter(email=email).first()

            if user is None:
                return ValidationError(
                    {
                        "status": "error",
                        "message": "User does not exist!",
                        "errors": f"User with email {email} does not exist!",
                    }
                )

            otp = generate_otp()
            otp_expiry = timezone.now() + timezone.timedelta(minutes=30)
            user.otp = otp
            user.otp_expiry = otp_expiry
            user.save()

            send_mail(
                "JE Express Password Reset",
                f"Your OTP is {otp}. Use it to reset your password.",
                None,
                [user.email],
                fail_silently=False,
            )

            return Response(
                {"message": "OTP sent to your email!"},
                status=status.HTTP_200_OK,
            )
        return ValidationError(serializer.errors)


class ResendOTP(APIView):
    """API endpoint for resending OTP."""

    serializer_class = ResendOTPSerializer

    @swagger_auto_schema(
        request_body=ResendOTPSerializer,
        responses={200: UserSerializer()},
    )
    def post(self, request):
        """Handle resending OTP."""
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.filter(email=email).first()

            if user is None:
                return ValidationError({"message": "User does not exist!"})

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
        return ValidationError(serializer.errors)


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
        """List all Apartment bookings by a user."""

        bookings = ApartmentBooking.objects.filter(user=request.user.id)
        serializer = ApartmentBookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivateAccount(APIView):
    """API endpoint for account activation."""

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
                return CustomException(
                    {
                        "message": f"User with email - {email} not found.",
                    },
                    404,
                )

            if user.is_active:
                return CustomException(
                    {
                        "message": "Account is already activated.",
                    },
                    400,
                )

            if user.otp != otp:
                return CustomException(
                    {
                        "message": "Invalid OTP.",
                    },
                    400,
                )

            if user.otp_expiry < timezone.now():
                return CustomException(
                    {
                        "message": "OTP has expired.",
                    },
                    400,
                )

            user.is_active = True
            user.otp = None
            user.otp_expiry = None
            user.save()
            return Response(
                {
                    "status": "success",
                    "message": "Account activated!",
                    "data": UserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )
        return CustomException(
            {
                "errors": serializer.errors,
            },
            400,
        )
