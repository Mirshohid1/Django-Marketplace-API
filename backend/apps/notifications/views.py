from django.db.models import QuerySet
from rest_framework.viewsets import ModelViewSet

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self) -> QuerySet[Notification]:
        if self.request.user.is_authenticated or self.request.user.is_superuser:
            return Notification.objects.filter(user=self.request.user)

        return Notification.objects.none()
