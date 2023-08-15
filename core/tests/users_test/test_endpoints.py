import pytest
from rest_framework.test import APIClient
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestUserEndpoints:

    def test_user_registration(self):
        client = APIClient()
        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = client.post("/api/user/register/", data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_user_login(self):
        client = APIClient()
        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        client.post("/api/user/register/", data)
        login_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        login_response = client.post("/api/user/login/", login_data)

        assert login_response.status_code == status.HTTP_200_OK


class FailTestUserEndpoints:

    @pytest.fixture
    def auth_client(self):
        client = APIClient()

        registration_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        registration_response = client.post("/api/user/register/", registration_data)
        assert registration_response.status_code == status.HTTP_201_CREATED

        client = registration_response
        return client

    def test_register_with_exist_email(self):
        client = APIClient()
        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = client.post("/api/user/register/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"email": "custom user with this email already exists."}

    def test_register_witout_at(self):
        client = APIClient()
        data = {
            "email": "testexample.com",
            "password": "testpassword",
        }
        response = client.post("/api/user/register/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"email": "Enter a valid email address."}

    def test_register_wrong_password_validation(self):
        client = APIClient()
        data = {
            "email": "testexample.com",
            "password": "1234567",
        }
        response = client.post("/api/user/register/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"Ensure this field has at least 8 characters."}

    def test_login_empty_information(self, auth_client):
        client = auth_client
        login_data = {
            "email": "",
            "password": "",
        }
        login_response = client.post("/api/user/login/", login_data)
        assert login_response.status_code == status.HTTP_400_BAD_REQUEST
        assert login_response.data == {
            "email": "This field may not be blank.",
            "password": "This field may not be blank."
        }

    def test_login_with_wrong_email(self, auth_client):
        client = auth_client
        login_data = {
            "email": "asdasd@asd.com",
            "password": "12345678",
        }
        login_response = client.post("/api/user/login/", login_data)
        assert login_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert login_response.data == {"error": "이메일 혹은 비밀번호가 유효하지 않습니다."}

    def test_login_with_wrong_password(self, auth_client):
        client = auth_client
        login_data = {
            "email": "test@example.com",
            "password": "12345678",
        }
        login_response = client.post("/api/user/login/", login_data)
        assert login_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert login_response.data == {"error": "이메일 혹은 비밀번호가 유효하지 않습니다."}
