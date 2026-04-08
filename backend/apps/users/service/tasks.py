from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from celery import shared_task
from ..models import EmailVerification


@transaction.atomic
def create_email_verification(user):
    EmailVerification.objects.filter(user=user).delete()
    verification = EmailVerification.objects.create(user=user)
    return verification

@shared_task
def send_email_verification(user_email, token, domain):
    relative_url = reverse("verify", kwargs={"token": token})
    absolute_url = f"http://{domain}{relative_url}"

    send_mail(
        "Verify your email",
        f"Click link: {absolute_url}",
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
    )