from django.db import transaction
from .models import EmailVerification


@transaction.atomic
def create_email_verification(user):
    EmailVerification.objects.filter(user=user).delete()
    verification = EmailVerification.objects.create(user=user)
    return verification

