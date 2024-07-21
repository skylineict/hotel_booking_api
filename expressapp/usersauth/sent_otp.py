import pyotp
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from .models import Customer,User, Manager  # Assuming Customer model is used for users
import pdb


def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=1800)  # OTP expires in 30 minutes (1800 seconds)
    return totp.now()


def email_otp_sent(email):
    user = None
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Handle case where user with the given email does not exist
        return False

    otp = generate_otp()
    try:
        user = Customer.objects.get(email=email)
        user.otp = otp
        user.otp_sent_time = timezone.now()
        user.save()
    except Customer.DoesNotExist:
                pass
    
    if not user:
        try:
             user = Manager.objects.get(email=email)
        except Manager.DoesNotExist:
            pass

    subject = "One Time Password (OTP) Generation"
    body = f"Hi {user.username}, Your OTP Verification code is: {otp}. This code expires in 30 minutes."

    email_from = settings.EMAIL_HOST_USER
    email_sent = EmailMessage(subject=subject, body=body, from_email=email_from, to=[email])
    email_sent.send(fail_silently=False)
    
