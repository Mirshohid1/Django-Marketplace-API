from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
from .managers import UserManager

import uuid


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=155,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9._-]+$',
                message='Username may contain only letters, numbers, dots, underscores and hyphens.'
            )
        ], blank=True, null=False
    )
    email = models.EmailField(max_length=155, unique=True)
    first_name = models.CharField(max_length=155, blank=True)
    last_name = models.CharField(max_length=155, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def generate_username(self):
        unique_id = str(uuid.uuid4())[:8]
        self.username = slugify(f"user-{unique_id}")

    def clean(self):
        super().clean()

        if self.first_name:
            self.first_name = " ".join(self.first_name.split())
        if self.last_name:
            self.last_name = " ".join(self.last_name.split())
        if self.email:
            self.email = self.email.strip().lower()

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.username:
            self.generate_username()

        super().save(*args, **kwargs)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


class EmailVerification(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='email_verification',
    )

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=30)
        super().save(*args, **kwargs)

    def is_expired(self):
        if not self.expires_at:
            return False
        return self.expires_at <= timezone.now()

    def __str__(self):
        return f"EmailVerification: {self.user}"

