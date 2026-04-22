from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from users.models import User

    from .models import Notification


def create_notification(
    user: User, notification_type: str, title: str, message: str, related_object_id=None
) -> Notification:
    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        related_object_id=related_object_id,
    )
