import pytest
from rest_framework import status


pytestmark = pytest.mark.django_db


class TestArticleEndpoints:

    @pytest.fixture
    def auth_client(self, api_client):
        client = api_client()

        # Register the user
        registration_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        client.post("/api/user/register/", registration_data)

        # Login with the registered user
        login_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = client.post("/api/user/login/", login_data)
        access_token = response.data['access_token']
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        return client

    def test_create_article(self, auth_client):
        # create article
        article_data = {
            "title": "Test Article",
            "content": "This is a test article.",
        }
        response = auth_client.post("/api/article/create_article/", article_data)
        assert response.status_code == status.HTTP_201_CREATED

        # update article
        article_id = response.data['id']
        update_data = {
            "title": "Updated Test Article",
            "content": "This is the updated test article content.",
        }
        update_response = auth_client.patch(
            f"/api/article/{article_id}/update_article/",
            update_data
        )
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data["title"] == update_data["title"]
        assert update_response.data["content"] == update_data["content"]
        # delete article
        delete_response = auth_client.delete(f"/api/article/{article_id}/delete_article/")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT


class TestFailArticleEndpoints:

    @pytest.fixture
    def auth_client_1(self, api_client):
        all_client = []
        for x in [0, 1]:
            client = api_client()
            # Register the user
            registration_data = {
                "email": f"test_{x}@example.com",
                "password": "testpassword",
            }
            client.post("/api/user/register/", registration_data)

            # Login with the registered user
            login_data = {
                "email": f"test_{x}@example.com",
                "password": "testpassword",
            }
            response = client.post("/api/user/login/", login_data)
            access_token = response.data['access_token']
            client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
            all_client.append(client)

        return all_client

    def test_create_empty_article(self, auth_client_1):
        auth_client_1 = auth_client_1[0]
        article_data = {
            "title": "",
            "content": "",
        }
        response = auth_client_1.post(
            "/api/article/create_article/",
            article_data,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_empty_article(self, auth_client_1):
        # create article
        article_data = {
            "title": "Test Article",
            "content": "This is a test article.",
        }
        response = auth_client_1[0].post("/api/article/create_article/", article_data)
        article_id = response.data['id']
        update_data = {
            "title": "",
            "content": "",
        }
        response = auth_client_1[0].patch(f"/api/article/{article_id}/update_article/", update_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_article_without_wrong_user(self, auth_client_1):
        # create article
        user_1 = auth_client_1[0]
        user_2 = auth_client_1[1]

        article_data = {
            "title": "Test Article",
            "content": "This is a test article.",
        }
        response = user_1.post("/api/article/create_article/", article_data)
        article_id = response.data['id']

        update_data = {
            "title": "123",
            "content": "123",
        }
        response = user_2.patch(
            f"/api/article/{article_id}/update_article/",
            update_data,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_nonexistent_article(self, auth_client_1):
        article_data = {
            "title": "Test Article",
            "content": "This is a test article.",
        }
        response = auth_client_1[0].post("/api/article/create_article/", article_data)
        article_id = response.data['id']
        auth_client_1[0].delete(
            f"/api/article/{article_id}/delete_article/"
        )
        delete_response = auth_client_1[0].delete(
            f"/api/article/{article_id}/delete_article/"
        )
        assert delete_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_article_wrong_user(self, auth_client_1):
        user_1 = auth_client_1[0]
        user_2 = auth_client_1[1]
        article_data = {
            "title": "Test Article",
            "content": "This is a test article.",
        }
        response = user_1.post("/api/article/create_article/", article_data)
        article_id = response.data['id']

        delete_response = user_2.patch(
            f"/api/article/{article_id}/update_article/",
        )

        assert delete_response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_nonexistent_article(self, auth_client_1):
        article_data = {
            "title": "Test Article",
            "content": "This is a test article.",
        }
        auth_client_1[0].post("/api/article/create_article/", article_data)
        nonexistent_article_id = 999999
        update_data = {
            "title": "123",
            "content": "123",
        }
        update_response = auth_client_1[0].patch(
            f"/api/article/{nonexistent_article_id}/update_article/",
            update_data,
        )

        assert update_response.status_code == status.HTTP_404_NOT_FOUND


class TestGetArticleList:

    @pytest.fixture
    def article_factory(self, article_factory):
        def create_article(title, content, author):
            return article_factory(title=title, content=content, author=author)
        return create_article

    def test_search_articles_list_with_pagination(
            self,
            article_factory,
            custom_user_factory,
            api_client
            ):

        client = api_client()
        for x in [0, 1]:
            article_factory(
                title=f"Article {x}",
                content=f"Content {x}",
                author=custom_user_factory(

                    email=f"asda{x}@asd.com",
                    password=f"password12{x}"
                )
            )

        response = client.get("/api/get_article/")
        assert response.status_code == status.HTTP_200_OK

        assert 'results' in response.data
        assert len(response.data['results']) == 2

        next_page_url = response.data['next']
        assert next_page_url is None
        if next_page_url is not None:
            response = client.get(next_page_url)
            assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_specific_article(self, article_factory, api_client, custom_user_factory):
        client = api_client()
        article = article_factory(
            "Specific Article",
            "Specific Content",
            custom_user_factory(
                email="asdasd@asd.com",
                password="passwordsd"
            )
        )
        article_id = article.id
        url = f"/api/get_article/{article_id}/"
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == "Specific Article"
        assert response.data['content'] == "Specific Content"
        article_id = article.id + 1
        url = f"/api/get_article/{article_id}/"
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
