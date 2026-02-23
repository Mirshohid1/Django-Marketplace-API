import pytest
from django.core.exceptions import ValidationError
from ..models import User
from ..serializers import RegisterSerializer


class TestRegisterSerializer():
    @pytest.fixture
    def valid_data(self):
        return {
            'username': 'User',
            'email': 'johndoe@example.com',
            'password': 'Strong_Password1234',
            'password_confirm': 'Strong_Password1234',
            'first_name': 'John',
            'last_name': 'Doe',
        }

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "field, value",
        [
            ('username', 'existing'),
            ('email', 'existing@example.com'),
        ]
    )
    def test_unique_fields(self, valid_data, field, value):
        data = valid_data.copy()
        data[field] = value

        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='Strong_Password1234',
        )

        serializer = RegisterSerializer(data=data)

        assert not serializer.is_valid()
        assert field in serializer.errors

    @pytest.mark.django_db
    def test_password_must_match(self, valid_data):
        data = valid_data.copy()
        data['password_confirm'] = 'password_2'

        serializer = RegisterSerializer(data=data)

        assert 'password' in serializer.errors

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "field, value",
        [
            ('password', 'wrong'),
            ('password', '3214',),
            ('password', 'Aa123456'),
            ('password', 'johndoe3214'),
        ]
    )
    def test_validate_password(self, valid_data, field, value):
        data = valid_data.copy()
        data[field] = value
        data['password_confirm'] = value

        serializer = RegisterSerializer(data=data)

        assert not serializer.is_valid()
        assert field in serializer.errors

    @pytest.mark.django_db
    def test_success_register(self, valid_data):
        data = valid_data.copy()

        serializer = RegisterSerializer(data=data)

        assert serializer.is_valid()
