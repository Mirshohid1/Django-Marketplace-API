from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from ..models import EmailVerification


@transaction.atomic
def create_email_verification(user):
    EmailVerification.objects.filter(user=user).delete()
    verification = EmailVerification.objects.create(user=user)
    return verification

def send_email_verification(user, token, request):
    relative_url = reverse(
        "verify-email",  # name из urls.py
        kwargs={"token": token}
    )

    absolute_url = request.build_absolute_uri(relative_url)

    send_mail(
        "Verify your email",
        f"Click link: {absolute_url}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
