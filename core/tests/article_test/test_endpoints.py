import pytest
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestArticleEndpoints:
    def test_create_post(self):
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

        # print(f"access_token : {response.data['access_token']}")

        # Create article
        access_token = response.data['access_token']
        article_endpoint = "/api/article/create_post/"
        data = {
            "title": "Test Article",
            "content": "This is a test article.",
        }
        article_response = client.post(
            article_endpoint,
            data,
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        if article_response.status_code == status.HTTP_301_MOVED_PERMANENTLY:
            redirect_url = article_response.url
            response = client.post(redirect_url, data, format="json")

        else:
            response = article_response

        assert article_response.status_code == status.HTTP_201_CREATED
