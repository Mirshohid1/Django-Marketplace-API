from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from users.views import RegisterAPIView


urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view(), name='register'),
]