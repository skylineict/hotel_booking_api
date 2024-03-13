import random
import string


def generate_username():
    """Generate a username with 12 lowercase chars prefixed with 'user_'."""
    random_string = "".join(random.choices(string.ascii_lowercase, k=12))
    return f"user_{random_string.lower()}"


def generate_otp():
    """Generate a 6-digit OTP."""
    return "".join(random.choices(string.digits, k=6))
