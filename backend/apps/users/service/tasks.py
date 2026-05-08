import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.urls import reverse

from ..models import EmailVerification

logger = logging.getLogger(__name__)


@transaction.atomic
def create_email_verification(user):
    logger.info("Task create_email_verification started")
    try:
        EmailVerification.objects.filter(user=user).delete()
        verification = EmailVerification.objects.create(user=user)
    except Exception:
        logger.exception("Task create_email_verification failed", extra={"user": user})
        raise
    return verification


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def send_email_verification(user_email, token, domain):
    logger.info(
        "Task send_email_verification started",
        extra={"user_email": user_email, "domain": domain},
    )

    try:
        relative_url = reverse("verify", kwargs={"token": token})
        absolute_url = f"http://{domain}{relative_url}"

        send_mail(
            "Verify your email",
            f"Click link: {absolute_url}",
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
        )
    except Exception:
        logger.exception(
            "Task send_email_verification failed",
            extra={"user_email": user_email, "domain": domain},
        )
        raise
    else:
        logger.info(
            "Task send_email_verification successful",
            extra={"user_email": user_email, "domain": domain},
        )
