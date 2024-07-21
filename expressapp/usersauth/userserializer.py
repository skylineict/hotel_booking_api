from rest_framework import serializers
from .models import Customer





class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=500, write_only=True)

    class Meta:
        model = Customer
        fields =['email', 'username', 'phone', 'password', 'first_name', 'last_name', 'dob']
    def create(self, validated_data):
        user = Customer.objects.create(**validated_data)
        return user


class Emailserializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields  = ['otp']


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=400, write_only=True)

    class Meta:
        model = Customer
        fields = ['email','password']

