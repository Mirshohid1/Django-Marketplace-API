from .models import Notification


def create_notification(user, type, title, message, related_object_id=None):
    return Notification.objects.create(
        user=user,
        type=type,
        title=title,
        message=message,
        related_object_id=related_object_id
    )