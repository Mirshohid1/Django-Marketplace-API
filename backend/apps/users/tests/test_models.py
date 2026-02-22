import pytest
import re
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ..models import User


@pytest.mark.django_db
def test_generate_username():
    user = User.objects.create_user(
        email='test1@example.com',
        password='test1234',
    )
    assert re.match(r"^user-[a-z0-9]+$", user.username)


@pytest.mark.django_db
def test_invalid_username():
    user = User(
        email='test2@example.com',
        username='Invalid username!',
    )
    user.set_password('test1234')

    with pytest.raises(ValidationError):
        user.save()


