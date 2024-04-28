""" This module contains the views for the user app. """

from django.contrib.auth import authenticate
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema  # pylint: disable=import-error
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from expressapp.utils import CustomResponse, CustomException

from .models import User
from .serializers import (
    UserSerializer,
    EmailVerificationSerializer,
    UserLoginSerializer,
    UserUpdateSerializer,
)


class UserSignup(APIView):
    """Create a new user account."""

    @swagger_auto_schema(
        operation_summary="Create a new user account.",
        request_body=UserSerializer,
        responses={201: UserSerializer()},
        security=[],
    )
    def post(self, request):
        """Create a new user account."""
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            user.generate_verification_otp()

            return Response(
                {
                    "status": "success",
                    "message": "Verification OTP sent to your email.",
                    "data": user_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return CustomException(user_serializer.errors, 400)


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
        user_serializer = UserSerializer(users, many=True)
        return CustomResponse(user_serializer.data, "List of all users", 200)


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
        user_serializer = UserSerializer(user)
        return CustomResponse(
            user_serializer.data, "User retrieved successfully", 200
        )


class UserUpdate(APIView):
    """Update the current user."""

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Update the current user.",
        request_body=UserUpdateSerializer,
        responses={200: UserSerializer()},
    )
    def put(self, request):
        """Update a user."""
        serializer = UserUpdateSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer = UserSerializer(request.user)

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
        security=[],
    )
    def post(self, request):
        """Handle user login."""
        login_serializer = UserLoginSerializer(data=request.data)
        if login_serializer.is_valid():
            email = login_serializer.validated_data["email"]
            password = login_serializer.validated_data["password"]

            user = authenticate(email=email, password=password)

            if not user:
                return CustomException("Invalid email or password", 401)

            if not user.email_verified:
                return CustomException("Email not verified", 401)

            if not user.is_active:
                return CustomException(
                    "Account is deactivated, contact admin", 401
                )

            user_data = UserSerializer(user).data
            access_token = RefreshToken.for_user(user).access_token
            user_data["access_token"] = str(access_token)
            return CustomResponse(user_data, "Logged in successfully", 200)
        return CustomException(login_serializer.errors, 400)


class EmailVerification(APIView):
    """API endpoint for email verification."""

    @swagger_auto_schema(
        operation_summary="Handle email verification.",
        request_body=EmailVerificationSerializer,
        responses={200: UserSerializer()},
        security=[],
    )
    def post(self, request):
        """Handle email verification."""
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            verification_otp = serializer.validated_data["verification_otp"]

            user = User.objects.filter(email=email).first()

            if not user:
                return CustomException("User does not exist!", 404)

            if user.email_verified:
                return CustomException("Email already verified!", 400)

            if user.verification_otp != verification_otp:
                return CustomException("Invalid OTP!", 400)

            if user.verification_otp_expiration < timezone.now():
                return CustomException("OTP has expired!", 400)

            user.email_verified = True
            user.verification_otp = None
            user.verification_otp_expiration = None
            user.save()
            return CustomResponse(
                UserSerializer(user).data, "Email verified successfully", 200
            )
        return CustomException(serializer.errors, 400)


class ForgotPassword(APIView):
    """API endpoint for handling forgot password."""

    @swagger_auto_schema(
        operation_summary="Handle forgot password.",
        request_body={"email": "string"},
        responses={200: UserSerializer()},
        security=[],
    )
    def post(self, request):
        """Handle forgot password."""
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            return CustomException("User does not exist!", 404)

        user.generate_reset_password_otp()
        return CustomResponse(
            {"message": "Reset password OTP sent to your email"}, 200
        )
