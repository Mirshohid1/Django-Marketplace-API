import pytest
import re
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from ..models import User, EmailVerification


class TestUserModel:
    @pytest.fixture
    def valid_data(self):
        return {
            'email': 'johndoe@example.com',
            'password': 'Strong_Password1234',
        }

    @pytest.mark.django_db
    def test_generate_username(self, valid_data):
        user = User.objects.create_user(
            email=valid_data['email'],
            password=valid_data['password'],
        )
        assert re.match(r"^user-[a-z0-9]+$", user.username)

    @pytest.mark.django_db
    def test_invalid_username(self, valid_data):
        user = User(
            email=valid_data['email'],
            username='Invalid username!',
        )
        user.set_password(valid_data['password'])

        with pytest.raises(ValidationError):
            user.save()

    @pytest.mark.django_db
    def test_normalize_fields(self, valid_data):
        user = User.objects.create_user(
            email="   " + valid_data['email'],
            first_name='  Test  .B   ',
            last_name='Test ',
            password=valid_data['password'],
        )
        assert user.email == valid_data['email']
        assert user.first_name == "Test .B"
        assert user.last_name == "Test"

    @pytest.mark.django_db
    def test_unique_email(self, valid_data):
        User.objects.create_user(
            email='existing@example.com',
            password=valid_data['password'],
        )

        with pytest.raises(ValidationError):
            User.objects.create_user(
                email='existing@example.com',
                password=valid_data['password'],
            )

@pytest.mark.django_db
class TestEmailVerificationModel:

    def test_expires_at_auto_set_on_save(self, user):
        verification = EmailVerification.objects.create(user=user)

        assert verification.expires_at is not None
        assert verification.expires_at > timezone.now()

    def test_is_expired_returns_false_when_valid(self, user):
        verification = EmailVerification.objects.create(user=user)

        assert verification.is_expired() is False

    def test_is_expired_returns_true_when_expired(self, user):
        verification = EmailVerification.objects.create(user=user)

        verification.expires_at = timezone.now() - timedelta(minutes=1)
        verification.save(update_fields=["expires_at"])

        assert verification.is_expired() is True

    def test_str_representation(self, user):
        verification = EmailVerification.objects.create(user=user)

        assert str(verification) == f"EmailVerification: {user}"