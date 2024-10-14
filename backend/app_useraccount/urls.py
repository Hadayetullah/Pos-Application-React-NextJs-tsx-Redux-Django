from django.urls import path
from .views import RegisterView, OTPVerifyView, LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),
    path('verify-otp/', OTPVerifyView.as_view(), name='api_verify_otp'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),

]
