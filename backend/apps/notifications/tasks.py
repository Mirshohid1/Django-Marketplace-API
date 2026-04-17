from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email_notification(email, title, message):
    send_mail(
        subject=title,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )
