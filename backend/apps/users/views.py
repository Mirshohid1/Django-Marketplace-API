import logging

from common.exceptions.base import NotFoundError, ValidationError
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from .models import EmailVerification
from .serializers import (
    LoginSerializer,
    LogoutSerializer,
    RegisterSerializer,
    UserOutPutSerializer,
    UserSerializer,
)
from .service.tasks import create_email_verification, send_email_verification

logger = logging.getLogger(__name__)


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        verification = create_email_verification(user)
        send_email_verification.delay(
            user.email, verification.token, self.request.get_host()
        )
        logger.info("User registered", extra={"id": user.id, "email": user.email})


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_authenticated:
            logger.info(
                "User authenticated",
                extra={"id": request.user.id, "email": request.user.email},
            )

        return Response(
            {
                "access": serializer.validated_data["access"],
                "refresh": serializer.validated_data["refresh"],
            },
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(
            "User logged out",
            extra={"id": request.user.id, "email": request.user.email},
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class MeAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserOutPutSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user


@extend_schema(
    request=None,
    responses={200: None},
    parameters=[
        OpenApiParameter(
            name="token",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description="Email verification token",
        ),
    ],
)
class VerifyEmailAPIView(APIView):

    authentication_classes: list[type[BaseAuthentication]] = []
    permission_classes: list[type[BasePermission]] = []

    def get(self, request, token):

        try:
            verification = EmailVerification.objects.select_related("user").get(
                token=token
            )
        except EmailVerification.DoesNotExist:
            logger.exception(
                "Token verification does not exist", extra={"token": token}
            )
            raise NotFoundError("Token verification does not exist") from None

        if verification.is_expired():
            verification.delete()
            logger.exception("Token expired", extra={"token": token})
            raise ValidationError("Token expired")

        user = verification.user
        user.is_verified = True
        user.save(update_fields=["is_verified"])

        verification.delete()

        logger.info("User verified", extra={"id": user.id, "email": user.email})

        return Response({"detail": "Email verified"}, status=status.HTTP_200_OK)


class ResendThrottle(UserRateThrottle):
    rate = "3/hour"


@extend_schema(
    request=None,
    responses={200: None},
)
class ResendVerificationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ResendThrottle]

    def post(self, request):
        user = request.user

        if user.is_verified:
            return Response(
                {"detail": "Email already verified"}, status=status.HTTP_400_BAD_REQUEST
            )

        verification = create_email_verification(user)
        send_email_verification.delay(
            user.email, verification.token, request.get_host()
        )

        logger.info(
            "Resend verification successful", extra={"id": user.id, "email": user.email}
        )
        return Response(
            {"detail": "Verification email sent"}, status=status.HTTP_200_OK
        )
