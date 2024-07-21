from rest_framework.generics import GenericAPIView
from .userserializer import Emailserializer
from .models import Customer,User,Manager
from rest_framework import status
from rest_framework.response import Response
from .sent_otp import email_otp_sent
import pdb



class EmailverifcationVeiw(GenericAPIView):
    serializer_class = Emailserializer

    def post(self, request):
        otp_verify_code = request.data.get('otp')
      
            # user = User.objects.get(otp=otp_verify_code) 
        if not otp_verify_code:
            return Response({'error': 'Verification code is not provided'}, status=status.HTTP_400_BAD_REQUEST)
        user = None
        try:
            # pdb.set_trace()
            user = Customer.objects.get(otp=otp_verify_code)
          
            if not user:
                return Response({'error': 'Account with provided OTP not found'}, status=status.HTTP_404_NOT_FOUND)
          
            if user.is_otp_expired():
                email_otp_sent(user.email)  # Generate and send new OTP
                return Response({'message': 'Verification code expired. New code sent to your email'}, status=status.HTTP_200_OK)
            if user.otp != otp_verify_code:
                return Response({'error': 'Invalid otp code'}, status=status.HTTP_400_BAD_REQUEST)
            if user.email_verified:
                return Response({'message': 'email already verified'}, status=status.HTTP_208_ALREADY_REPORTED)
            user.email_verified = True
            user.is_customer = True
            user.save()
            return Response({'success': 'email verified'}, status=status.HTTP_201_CREATED)

        except Customer.DoesNotExist:
            pass      
        if not user:
            try:

                user = Manager.objects.get(otp=otp_verify_code)
                if user.is_otp_expired():
                    email_otp_sent(user.email)  # Generate and send new OTP
                    return Response({'message': 'Verification code expired. New code sent to your email'}, status=status.HTTP_200_OK)
                if user.otp != otp_verify_code:
                    return Response({'error': 'Invalid otp code'}, status=status.HTTP_400_BAD_REQUEST)
                if user.email_verified:
                    return Response({'message': 'email already verified'}, status=status.HTTP_208_ALREADY_REPORTED)
                user.email_verified = True
                user.is_manager = True
                user.save()
                return Response({'success': 'email verified'}, status=status.HTTP_201_CREATED)
            except Manager.DoesNotExist:
                return Response({'message':'account with provided otp not found'}, status=status.HTTP_404_NOT_FOUND)


        
         
                   
    
           
               
           
                 