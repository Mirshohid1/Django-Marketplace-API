from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken
from ..models import User

import pytest


@pytest.mark.django_db
class TestRegisterAPIView:
    def test_register_success(self, api_client):
        url = reverse('register')

        data = {
            'email': 'johndoe@example.com',
            'password': 'Strong_Password1234',
            'password_confirm': 'Strong_Password1234',
        }

        response = api_client.post(url, data)

        assert response.status_code == 201
        assert User.objects.filter(email='johndoe@example.com').exists()

        user = User.objects.get(email='johndoe@example.com')
        assert user.check_password('Strong_Password1234')

    @pytest.mark.parametrize(
        'email, password, password_confirm',
        [
            ('invalid_email', 'Strong_Password1234', 'Strong_Password1234'),
            ('', 'Strong_Password1234', 'Strong_Password1234'),
            ('wrong@example.com', 'short', 'short'),
            ('wrong2@example.com', 'Strong_Password1234', 'Different_Password1234'),
        ]
    )
    def test_register_invalid_data(
            self, api_client, email, password, password_confirm
    ):
        url = reverse('register')

        response = api_client.post(url, {
            'email': email,
            'password': password,
            'password_confirm': password_confirm,
        })

        assert response.status_code == 400


@pytest.mark.django_db
class TestLoginAPIView:
    def test_success_login(self, api_client, user):
        url = reverse('login')

        response = api_client.post(url,{
            'login': "existing@example.com",
            'password': 'Strong_Password1234',
        })

        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

        access = AccessToken(response.data['access'])
        assert access['user_id'] == str(user.id)

    @pytest.mark.parametrize(
        'login, password',
        [
            ('not_existing', 'Strong_Password1234'),
            ('not_existing@example.com', 'Strong_Password1234'),
            ('existing', 'Wrong_Password1234'),
            ('existing@example.com', 'Wrong_Password1234'),
        ]
    )
    def test_unsuccess_login(self, api_client, login, password, user):
        url = reverse('login')

        response = api_client.post(url,{
            'login': login,
            'password': password,
        })

        assert response.status_code == 400
        assert 'non_field_errors' in response.data
        assert response.data['non_field_errors'][0] == "Invalid credentials."


@pytest.mark.django_db
class TestLogoutAPIView:
    def test_logout_unauthorized(self, api_client):
        url = reverse('logout')
        response = api_client.post(url)
        assert response.status_code == 401

    def test_logout_success(self, api_client, user):
        api_client.force_authenticate(user=user)
        refresh = str(RefreshToken.for_user(user))

        url = reverse('logout')
        response = api_client.post(url, {'refresh': refresh})

        assert response.status_code == 204

        from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
        token = OutstandingToken.objects.get(token=refresh)
        assert BlacklistedToken.objects.filter(token=token).exists()

    def test_logout_invalid_token(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('logout')
        response = api_client.post(url, {'refresh': 'wrong_token'})

        assert response.status_code == 400
        assert 'Invalid token.' in str(response.data)


@pytest.mark.django_db
class TestMeAPIView:
    def test_me_unauthorized(self, api_client):
        url = reverse('me')
        response = api_client.get(url)

        assert response.status_code == 401

    def test_me_get_success(self, api_client, user):
        api_client.force_authenticate(user=user)

        url = reverse('me')
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data['id'] == user.id
        assert response.data['email'] == user.email
        assert 'password' not in response.data

    def test_me_update_success(self, api_client, user):
        api_client.force_authenticate(user=user)

        url = reverse('me')
        response = api_client.patch(url, {
            'first_name': 'Updated',
        })

        assert response.status_code == 200

        user.refresh_from_db()
        assert user.first_name == 'Updated'

    def test_me_update_fail(self, api_client, user):
        api_client.force_authenticate(user=user)

        url = reverse('me')
        response = api_client.patch(url, {
            'id': 99
        })

        assert response.status_code == 400
        assert 'id' in response.data

    def test_me_update_unauthorized(self, api_client, user):
        url = reverse('me')
        response = api_client.patch(url, {
            'first_name': 'Updated',
        })

        assert response.status_code == 401
