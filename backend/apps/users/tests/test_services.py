import pytest
from django.core.exceptions import ValidationError

from ..service.validators import PasswordValidationService


class TestPasswordValidationService:
    @pytest.mark.parametrize(
        "password, field_name, field_value",
        [
            ("user1234", "username", "User"),
            ("john1234", "first_name", "John"),
            ("doe1234", "last_name", "Doe"),
            ("johndoe12345", "email", "johndoe@example.com"),
            ("johndoe", "email", "johndoe@example.com")
        ],
    )
    def test_password_similarity(self, password, field_name, field_value):
        kwargs = {field_name: field_value}

        with pytest.raises(ValidationError):
            PasswordValidationService.validate(password, **kwargs)

    def test_password_valid_with_missing_optional_fields(self):
        PasswordValidationService.validate(
            password="StrongPassword123!"
        )

    def test_error_message_content(self):
        with pytest.raises(ValidationError) as exc:
            PasswordValidationService.validate(
                password="john",
                first_name="John",
            )

        assert "too similar" in str(exc.value)

