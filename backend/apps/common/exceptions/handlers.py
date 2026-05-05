import logging

from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .base import DomainError

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # 1. Наши ошибки
    if isinstance(exc, DomainError):
        return Response(
            {
                "error": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
            status=exc.status_code,
        )

    # 2. DRF ValidationError → приводим к нашему формату
    if isinstance(exc, DRFValidationError):
        return Response(
            {
                "error": "validation_error",
                "message": "Invalid data",
                "details": exc.detail,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 3. стандартный handler DRF
    response = exception_handler(exc, context)
    if response is not None:
        return response

    # 4. неизвестные ошибки
    logger.exception("Unhandled exception", exc_info=exc)

    return Response(
        {
            "error": "internal_error",
            "message": "Internal server error",
            "details": None,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
