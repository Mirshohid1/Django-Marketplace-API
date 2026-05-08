import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def send_email_notification(email, title, message):
    logger.info("Task send_email_notification started")
    try:
        send_mail(
            subject=title,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        logger.info("Task send_email_notification successful")
    except Exception as e:
        logger.exception(
            "Task send_email_notification failed",
            extra={"email": email, "error": str(e)},
        )
        raise
