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
        assert reponse.data['non_field_errors'][0] == "Invalid credentials."
