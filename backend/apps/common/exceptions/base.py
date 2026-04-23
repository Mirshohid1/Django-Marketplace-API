from rest_framework import status
from rest_framework.exceptions import APIException


class DomainException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Internal server error"
    default_code = "internal_server_error"
