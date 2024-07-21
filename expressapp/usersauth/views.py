from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .userserializer import CustomerSerializer,LoginSerializer
from .sent_otp import email_otp_sent
from django.contrib.auth import authenticate
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta

# Create your views here.
import pdb

class CustomerRegistration(GenericAPIView):
    serializer_class = CustomerSerializer
    def post(self, request):
        serializer_data = CustomerSerializer(data=request.data)
        # pdb.set_trace()
        if serializer_data.is_valid():
            user_instance =serializer_data.save()
            user_email = serializer_data.data.get('email')
           
            # print('hello my email', user_email)
            try: 
                email_otp_sent(user_email)
                return Response({
                      'success': "Account created. OTP has been sent to your email.", 
                      'data': serializer_data.data
                      },status=status.HTTP_201_CREATED)
            
            except Exception as e:
                  
                #   if 'user_instance' in locals() or 'user_instance' in globals():
                    user_instance.delete()
                    return Response({'errro': f"Failed to sent OTP email to {user_email} it doenst exist"},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
    

class Login(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user  is None:
              return Response({"error": "invalid email or pasword"}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(email=email).exists():
             return Response({'message': "Email not found "}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.email_verified:
              email_otp_sent(user.email)
              return Response({'message': "Email is not verified, kindly, otp has been sent to your email to verify and continue logging "}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.check_password(password):
            return Response({'message': "Incorrect password "}, status=status.HTTP_401_UNAUTHORIZED)
        refresh_token  = RefreshToken.for_user(user)
        refresh_token.set_exp(lifetime=timedelta(days=30))
        res = Response()
        res.set_cookie(key='token', value=str(refresh_token.access_token), httponly=True)
        res.data = {
              "email": user.email,
             "username": user.username,
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token),
           

        }
        




        
     




        









