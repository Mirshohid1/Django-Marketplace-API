import pytest
from ..models import User
from ..serializers import RegisterSerializer, LoginSerializer


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='existing',
        email='existing@example.com',
        password='Strong_Password1234',
    )


@pytest.mark.django_db
class TestRegisterSerializer:
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

    @pytest.mark.parametrize(
        "field, value",
        [
            ('username', 'existing'),
            ('email', 'existing@example.com'),
        ]
    )
    def test_unique_fields(self, valid_data, field, value, user):
        data = valid_data.copy()
        data[field] = value

        serializer = RegisterSerializer(data=data)

        assert not serializer.is_valid()
        assert field in serializer.errors

    def test_password_must_match(self, valid_data):
        data = valid_data.copy()
        data['password_confirm'] = 'password_2'

        serializer = RegisterSerializer(data=data)

        assert not serializer.is_valid()
        assert 'password' in serializer.errors

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

    def test_success_register(self, valid_data):
        data = valid_data.copy()

        serializer = RegisterSerializer(data=data)

        assert serializer.is_valid()


@pytest.mark.django_db
class TestLoginSerializer:
    @pytest.mark.parametrize("login, password", [
        ('existing', 'Strong_Password1234'),
        ('existing@example.com', 'Strong_Password1234'),
    ]
    )
    def test_success_login(self, login, password, user):
        serializer = LoginSerializer(data={
            'login': login,
            'password': password,
        })

        assert serializer.is_valid()

        assert 'access' in serializer.validated_data
        assert 'refresh' in serializer.validated_data

    @pytest.mark.parametrize("login, password", [
        ('not_existing', 'Strong_Password1234'),
        ('not_existing@example.com', 'Strong_Password1234'),
        ('existing', 'Wrong_Password1234'),
        ('existing@example.com', 'Wrong_Password1234'),
    ]
    )
    def test_unsuccess_login(self, login, password, user):
        serializer = LoginSerializer(data={
            'login': login,
            'password': password,
        })

        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors
