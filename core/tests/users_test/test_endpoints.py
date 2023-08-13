import pytest
from rest_framework.test import APIClient
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestUserEndpoints:

    def test_user_registration(self):
        register_endpoint = "/api/user/register/"
        client = APIClient()
        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = client.post(register_endpoint, data)

        if response.status_code == status.HTTP_301_MOVED_PERMANENTLY:
            redirect_url = response.url
            response = client.post(redirect_url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED

    def test_user_login(self):
        register_endpoint = "/api/user/register/"
        login_endpoint = "/api/user/login/"

        # Register the user
        client = APIClient()
        registration_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        registration_response = client.post(register_endpoint, registration_data)
        if registration_response.status_code == status.HTTP_301_MOVED_PERMANENTLY:
            redirect_url = registration_response.url
            response = client.post(redirect_url, registration_data, format="json")
        else:
            response = registration_response

        assert response.status_code == status.HTTP_201_CREATED

        # Login with the registered user
        login_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        login_response = client.post(login_endpoint, login_data)
        if login_response.status_code == status.HTTP_301_MOVED_PERMANENTLY:
            redirect_url = login_response.url
            response = client.post(redirect_url, login_data, format="json")
        else:
            response = login_response

        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.data
        assert "refresh_token" in response.data

        # Login with wrong email
        login_data = {
            "email": "test1@exaas.com",
            "password": "testpassword",
        }
        login_response = client.post(login_endpoint, login_data)
        if login_response.status_code == status.HTTP_301_MOVED_PERMANENTLY:
            redirect_url = login_response.url
            response = client.post(redirect_url, login_data, format="json")
        else:
            response = login_response
        assert response.data == {'error': '이메일 혹은 비밀번호가 유효하지 않습니다.'}
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Login with wrong password
        login_data = {
            "email": "test@example.com",
            "password": "testpasswor222d",
        }
        login_response = client.post(login_endpoint, login_data)
        if login_response.status_code == status.HTTP_301_MOVED_PERMANENTLY:
            redirect_url = login_response.url
            response = client.post(redirect_url, login_data, format="json")
        else:
            response = login_response
        assert response.data == {'error': '이메일 혹은 비밀번호가 유효하지 않습니다.'}
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
