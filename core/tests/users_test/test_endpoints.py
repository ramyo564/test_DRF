import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestUserEndpoints:

    def test_user_registration(self, api_client):

        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = api_client().post("/api/user/register/", data)

        assert response.status_code == status.HTTP_201_CREATED
        client = response
        return client

    def test_user_login(self, api_client):

        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        api_client().post("/api/user/register/", data)
        login_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        login_response = api_client().post("/api/user/login/", login_data)

        assert login_response.status_code == status.HTTP_200_OK


class TestFailUserEndpoints:

    def test_register_with_exist_email(self, api_client, custom_user_factory):
        user = custom_user_factory.create_batch(1)[0]

        data = {
            "email": user.email,
            "password": custom_user_factory(password="12345678"),
        }
        response = api_client().post("/api/user/register/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_witout_at(self, api_client, custom_user_factory):
        data = {
            "email": custom_user_factory(email="asdad.com"),
            "password": "testpassword",
        }
        response = api_client().post("/api/user/register/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_wrong_password_validation(self, api_client):
        data = {
            "email": "asdasdasd@asdasd.com",
            "password": "1234567",
        }
        response = api_client().post("/api/user/register/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_empty_information(self, api_client):
        login_data = {
            "email": "",
            "password": "",
        }
        login_response = api_client().post("/api/user/login/", login_data)
        assert login_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_with_nonexist_email(self, api_client):

        login_data = {
            "email": "asdasd@asd.com",
            "password": "12345678",
        }
        login_response = api_client().post("/api/user/login/", login_data)
        assert login_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_with_wrong_password(self, api_client, custom_user_factory):
        user = custom_user_factory.create_batch(1)[0]
        data = {
            "email": user.email,
            "password": "12345678",
        }
        response = api_client().post("/api/user/login/", data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
