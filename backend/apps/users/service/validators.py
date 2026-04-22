from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class PasswordSimilarityValidator:

    @staticmethod
    def validate(
        password: str, username=None, email=None, first_name=None, last_name=None
    ) -> None:
        forbidden_values = []

        if username:
            forbidden_values.append(username)
        if first_name:
            forbidden_values.append(first_name)
        if last_name:
            forbidden_values.append(last_name)

        if email:
            local_part = email.split("@")[0]
            forbidden_values.append(local_part)

        password_lower = password.lower()

        for value in forbidden_values:
            if value.lower() in password_lower or password_lower in value.lower():
                raise ValidationError("Password is too similar to personal information")


class PasswordValidationService:

    @staticmethod
    def validate(
        password: str, username=None, email=None, first_name=None, last_name=None
    ) -> None:
        PasswordSimilarityValidator.validate(
            password, username, email, first_name, last_name
        )

        validate_password(password)
