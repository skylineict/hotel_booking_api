""" This module contains the views for the user app. """

from django.contrib.auth import authenticate
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema  # pylint: disable=import-error
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from expressapp.utils import CustomResponse, CustomException

from .models import User, ResetPassword
from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    UserUpdateSerializer,
    EmailVerificationSerializer,
    ValidateResetOTPSerializer,
    ResetPasswordSerializer,
    ResendOTPSerializer,
)


class UserSignup(APIView):
    """Create a new user account."""

    @swagger_auto_schema(
        operation_summary="Create a new user account.",
        request_body=UserSerializer,
        responses={201: UserSerializer()},
        security=[],
        order=1,
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


class VendorSignup(APIView):
    """Create a new vendor account."""

    @swagger_auto_schema(
        operation_summary="Create a new vendor account.",
        request_body=UserSerializer,
        responses={201: UserSerializer()},
        security=[],
    )
    def post(self, request):
        """Create a new vendor account."""
        vendor_serializer = UserSerializer(data=request.data)
        if vendor_serializer.is_valid():
            vendor_serializer.validated_data["is_vendor"] = True
            vendor = vendor_serializer.save()
            vendor.generate_verification_otp()

            return Response(
                {
                    "status": "success",
                    "message": "Verification OTP sent to your email.",
                    "data": vendor_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return CustomException(vendor_serializer.errors, 400)


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

            if user.is_suspended:
                return CustomException("Suspended account: Please contact support", 401)

            user_data = UserSerializer(user).data
            access_token = RefreshToken.for_user(user).access_token
            user_data["access_token"] = str(access_token)
            return CustomResponse(user_data, "Logged in successfully", 200)
        return CustomException(login_serializer.errors, 400)


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
            return CustomException(f"{user_id or request.user.id} not found", 404)
        user_serializer = UserSerializer(user)
        return CustomResponse(user_serializer.data, "User retrieved successfully", 200)


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

            return CustomResponse(serializer.data, "User updated successfully", 200)
        return CustomException(serializer.errors, 400)


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
                return CustomException("Verification OTP has expired!", 400)

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
        responses={200: ()},
        security=[],
    )
    def post(self, request, email):
        """Handle forgot password."""
        user = User.objects.filter(email=email).first()

        if not user:
            return CustomException("User does not exist!", 404)

        user.generate_reset_password_otp()
        return CustomResponse({"message": "Reset password OTP sent to your email"}, 200)


class ValidateResetOTP(APIView):
    """API endpoint for validating Reset Password OTP"""

    @swagger_auto_schema(
        operation_summary="Valildates Reset Password OTP.",
        request_body=ValidateResetOTPSerializer,
        responses={200: UserSerializer()},
        security=[],
    )
    def post(self, request):
        """Valildates Reset Password OTP."""
        serializer = ValidateResetOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            reset_password_otp = serializer.validated_data["reset_password_otp"]

            user = User.objects.filter(email=email).first()

            if not user:
                return CustomException("User does not exist!", 404)

            if user.reset_password_otp != reset_password_otp:
                return CustomException("Invalid OTP!", 400)

            if user.reset_password_otp_expiration < timezone.now():
                return CustomException("Reset Password OTP has expired!", 400)

            user.reset_password_otp = None
            user.reset_password_otp_expiration = None
            user.save()

            reset_password = ResetPassword(user=user)
            reset_password.save()

            user_data = UserSerializer(user).data
            user_data["reset_password_token"] = str(reset_password.reset_password_token)

            return CustomResponse(
                user_data, "Reset Password OTP verified successfully", 200
            )
        return CustomException(serializer.errors, 400)


class ResetPasswordView(APIView):
    """API endpoint for Resetting User's Password"""

    @swagger_auto_schema(
        operation_summary="Resets User Password.",
        request_body=ResetPasswordSerializer,
        responses={200: UserSerializer()},
        security=[],
    )
    def post(self, request):
        """Valildates Reset Password OTP."""
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            reset_password_token = serializer.validated_data["reset_password_token"]
            new_password = serializer.validated_data["new_password"]

            reset_password = ResetPassword.objects.filter(
                reset_password_token=reset_password_token
            ).first()

            if not reset_password:
                return CustomException("Invalid Reset Password Token!", 404)

            if reset_password.expiration_time < timezone.now():
                return CustomException("Reset Password Token has expired!", 400)

            reset_password.save()

            user = reset_password.user
            user.set_password(new_password)
            user.save()

            return CustomResponse(
                UserSerializer(user).data, "Password changed successfully", 200
            )
        return CustomException(serializer.errors, 400)


class ResendOTP(APIView):
    """API Endpoint to Resend a OTP"""

    @swagger_auto_schema(
        operation_summary="Resends OTP.",
        request_body=ResendOTPSerializer,
        responses={200: ()},
        security=[],
    )
    def post(self, request):
        """Resends OTP."""
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            purpose = serializer.validated_data["purpose"]

            user = User.objects.filter(email=email).first()

            if not user:
                return CustomException("User does not exist!", 404)

            if purpose == "verification":
                user.generate_verification_otp()
                return CustomResponse(
                    None,
                    "Email Verification OTP sent to your email",
                    200,
                )
            elif purpose == "reset-password":
                user.generate_reset_password_otp()
                return CustomResponse("Reset password OTP sent to your email", 200)
            else:
                return CustomException("Invalid Choice of Purpose", 400)
        return CustomException(serializer.errors, 400)


class ActivateUser(APIView):
    """API Endpoint to Suspend a User"""

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Suspend a User.",
        responses={200: UserSerializer()},
    )
    def post(self, request, user_id: str):
        """Suspend a User."""
        user = User.objects.filter(id=user_id).first()
        if not user:
            return CustomException(f"{user_id} not found", 404)
        user.is_suspended = False
        user.save()
        return CustomResponse(
            UserSerializer(user).data, "User suspended successfully", 200
        )


class DeactivateUser(APIView):
    """API Endpoint to Unsuspend a User"""

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Unsuspend a User.",
        responses={200: UserSerializer()},
    )
    def post(self, request, user_id: str):
        """Unsuspend a User."""
        user = User.objects.filter(id=user_id).first()
        if not user:
            return CustomException(f"{user_id} not found", 404)
        user.is_suspended = True
        user.save()
        return CustomResponse(
            UserSerializer(user).data, "User unsuspended successfully", 200
        )
