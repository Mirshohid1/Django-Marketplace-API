from django.db import models
from users.models import User


class Notification(models.Model):
    class Types(models.TextChoices):
        ORDER_CREATED = "order_created"
        ORDER_PAID = "order_paid"
        ORDER_SHIPPED = "order_shipped"
        SYSTEM = "system"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    notification_type = models.CharField(
        max_length=50, choices=Types.choices, db_column="type"
    )
    title = models.CharField(max_length=255)
    message = models.TextField()

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    related_object_id = models.UUIDField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.notification_type}"
