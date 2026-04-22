from django.db.models import QuerySet
from rest_framework.viewsets import ModelViewSet

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self) -> QuerySet[Notification]:
        return Notification.objects.filter(user=self.request.user)
