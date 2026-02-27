from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from ..models import EmailVerification


@transaction.atomic
def create_email_verification(user):
    EmailVerification.objects.filter(user=user).delete()
    verification = EmailVerification.objects.create(user=user)
    return verification

def send_email_verification(user, token):
    verification_url = (
        f"http://localhost:8000/api/auth/verify/{token}/"
    )

    send_mail(
        subject="Email Verification",
        message=f"Verify your email: {verification_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
