from django.contrib.auth.models import User
import pytest


@pytest.mark.django_db
class TestAccounts:

    def test_registration(self, client):
        response = client.get('/accounts/register')
        assert response.status_code == 200

        assert 0 == User.objects.all().count()

        params = {
            'username': 'john',
            'password1': '12345678Qq',
            'password2': '12345678Qq',
        }
        response = client.post('/accounts/register', params)
        user = User.objects.filter(username="john")
        assert 1 == user.count() and user.exists()

    def test_login(self, client):

        params = {
            'username': 'john',
            'password1': '12345678Qq',
            'password2': '12345678Qq',
        }
        response = client.post('/accounts/register', params)
        params = {
            'username': 'john',
            'password': '12345678Qq',
        }
        response = client.post('/accounts/sign-in', params)
        assert response.status_code == 302

        response = client.get('/')
        assert response.status_code == 200
        assert "john" in str(response.content)

    def test_login(self, client):
        params = {
            'username': 'john',
            'password1': '12345678Qq',
            'password2': '12345678Qq',
        }
        response = client.post('/accounts/register', params)
        params = {
            'username': 'john',
            'password': '12345678Qq',
        }
        response = client.post('/accounts/sign-in', params)

        response = client.get('/')
        assert response.status_code == 200

        response = client.get('/accounts/logout')

        response = client.get('/')
        assert response.status_code == 302
