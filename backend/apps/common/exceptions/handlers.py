from rest_framework import status
from rest_framework.exceptions import APIException


class DomainException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A domain error occurred."
    default_code = "domain_error"
