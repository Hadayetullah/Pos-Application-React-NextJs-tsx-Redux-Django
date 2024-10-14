from django.conf import settings
from django.utils import timezone

from django.contrib.auth import authenticate

from rest_framework import serializers
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'password']
    

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            phone=validated_data['phone'],
        )
        user.set_password(validated_data['password'])
        user.is_active = False  # User is inactive until OTP is verified
        user.otp = get_random_string(length=6, allowed_chars='0123456789')
        user.otp_created_at = timezone.now()
        user.save()

        # Send OTP to the user's email
        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP code is {user.otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return user




class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        if user.otp != data['otp']:
            raise serializers.ValidationError("Invalid OTP.")
        if not user.otp_is_valid():
            raise serializers.ValidationError("OTP expired.")

        return data

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.is_active = True  # Activate the user
        user.otp = None  # Clear the OTP after verification
        user.save()

        return user
    


