import random
import string
from django.core.mail import send_mail
from django.utils import timezone


def generate_username():
    """Generate a username with 12 lowercase chars prefixed with 'user_'."""
    random_string = "".join(random.choices(string.ascii_lowercase, k=12))
    return f"user_{random_string.lower()}"


def generate_otp():
    """Generate a 6-digit OTP."""
    return "".join(random.choices(string.digits, k=6))


def send_otp(user):
    """Send OTP to the user."""
    otp = generate_otp()
    user.otp = otp
    user.otp_expiry = timezone.now() + timezone.timedelta(minutes=30)
    user.save()
    send_mail(
        "JE Express Account Activation",
        f"Your OTP is {otp}. Use it to activate your account.",
        None,
        [user.email],
    )
