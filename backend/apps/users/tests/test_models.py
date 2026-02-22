import pytest
import re
from ..models import User


@pytest.mark.django_db
def test_generate_username():
    user = User.objects.create_user(
        email='test1@example.com',
        password='test1234',
    )
    assert re.match(r"^user-[a-z0-9]+$", user.username)

