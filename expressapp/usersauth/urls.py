from django.urls import path
from .views import CustomerRegistration,Login
from .email_verification import EmailverifcationVeiw
# from .passwordReset  import PasswordResetView, PasswordcomfirmReset,SetPasswordView,Logoutveiw
urlpatterns = [
     path('customer-singup', CustomerRegistration.as_view(), name='singup'),
     path('email-verify', EmailverifcationVeiw.as_view(), name='email_verify'),
      path('Login', Login.as_view(), name='login')
       
]