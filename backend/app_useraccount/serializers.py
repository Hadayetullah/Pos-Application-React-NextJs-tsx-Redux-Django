from django.conf import settings
from django.utils import timezone

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
