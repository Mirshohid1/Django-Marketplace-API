from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from users.views import RegisterAPIView, LoginAPIView, MeAPIView, LogoutAPIView


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeAPIView.as_view(), name='me'),
]