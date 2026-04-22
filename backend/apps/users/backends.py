from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.request import Request

User = get_user_model()


class EmailOrUsernameBackend(ModelBackend):

    def authenticate(
        self, request: Request, username=None, password=None, **kwargs: Any
    ):
        try:
            user = User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
