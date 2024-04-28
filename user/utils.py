import random
import string


def generate_otp():
    """Generate a 6-digit OTP."""
    return "".join(random.choices(string.digits, k=6))
