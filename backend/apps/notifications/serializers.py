from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "id",
            "notification_type",
            "user",
            "title",
            "message",
            "is_read",
            "created_at",
            "updated_at",
            "related_object_id",
        )
        read_only_fields = ("id", "created_at", "updated_at", "related_object_id")
