from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from .service.email import create_email_verification, send_email_verification
from .models import EmailVerification

from .serializers import (
    RegisterSerializer, LoginSerializer, LogoutSerializer,
    UserSerializer, UserOutPutSerializer
)


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        verification = create_email_verification(user)
        send_email_verification(user, verification.token)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            "access": serializer.validated_data["access"],
            "refresh": serializer.validated_data["refresh"],
        }, status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserOutPutSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user


class VerifyEmailAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, token):

        try:
            verification = EmailVerification.objects.select_related("user").get(token=token)
        except EmailVerification.DoesNotExist:
            return Response(
                {"detail": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if verification.is_expired():
            verification.delete()
            return Response(
                {"detail": "Token expired"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = verification.user
        user.is_verified = True
        user.save(update_fields=["is_verified"])

        verification.delete()

        return Response(
            {"detail": "Email verified"},
            status=status.HTTP_200_OK
        )


class ResendThrottle(UserRateThrottle):
    rate = "3/hour"


class ResendVerificationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ResendThrottle]

    def post(self, request):
        user = request.user

        if user.is_verified:
            return Response(
                {"detail": "Email already verified"},
                status=status.HTTP_400_BAD_REQUEST
            )

        verification = create_email_verification(user)
        send_email_verification(user, verification.token)

        return Response(
            {"detail": "Verification email sent"},
            status=status.HTTP_200_OK
        )
