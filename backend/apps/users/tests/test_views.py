from django.urls import reverse
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
