from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from users.views import (
    RegisterAPIView, LoginAPIView,
    MeAPIView, LogoutAPIView,
    VerifyEmailAPIView, ResendVerificationAPIView
)


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeAPIView.as_view(), name='me'),
    path('verify/<uuid:token>/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('resend_verification/', ResendVerificationAPIView.as_view(), name='resend_verification'),
]