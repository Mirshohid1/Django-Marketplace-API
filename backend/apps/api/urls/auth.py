from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from users.views import RegisterAPIView, LoginAPIView


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view(), name='register'),
]