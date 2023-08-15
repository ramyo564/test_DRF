# import pytest
# from rest_framework import status
# from rest_framework.test import APIClient
# from django.urls import reverse
# pytestmark = pytest.mark.django_db


# class TestArticleEndpoints:

#     @pytest.fixture
#     def auth_client(self):
#         client = APIClient()

#         # Register the user
#         registration_data = {
#             "email": "test@example.com",
#             "password": "testpassword",
#         }
#         client.post("/api/user/register/", registration_data)

#         # Login with the registered user
#         login_data = {
#             "email": "test@example.com",
#             "password": "testpassword",
#         }
#         response = client.post("/api/user/login/", login_data)
#         access_token = response.data['access_token']
#         client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

#         return client

#     def test_create_article(self, auth_client):
#         # create article
#         article_data = {
#             "title": "Test Article",
#             "content": "This is a test article.",
#         }
#         response = auth_client.post("/api/article/create_article/", article_data)
#         assert response.status_code == status.HTTP_201_CREATED

#         # update article
#         article_id = response.data['id']
#         update_data = {
#             "title": "Updated Test Article",
#             "content": "This is the updated test article content.",
#         }
#         update_response = auth_client.patch(
#             f"/api/article/{article_id}/update_article/",
#             update_data
#         )
#         assert update_response.status_code == status.HTTP_200_OK
#         assert update_response.data["title"] == update_data["title"]
#         assert update_response.data["content"] == update_data["content"]

#         # delete article
#         delete_response = auth_client.delete(f"/api/article/{article_id}/delete_article/")
#         assert delete_response.status_code == status.HTTP_204_NO_CONTENT


# class FailTestArticleEndpoints:

#     @pytest.fixture
#     def auth_client_1(self):
#         client = APIClient()

#         registration_data = {
#             "email": "test@example.com",
#             "password": "testpassword",
#         }
#         registration_response = client.post("/api/user/register/", registration_data)
#         assert registration_response.status_code == status.HTTP_201_CREATED

#         login_data = {
#             "email": "test@example.com",
#             "password": "testpassword",
#         }
#         login_response = client.post("/api/user/login/", login_data)
#         assert login_response.status_code == status.HTTP_200_OK

#         access_token = login_response.data['access_token']
#         client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

#         return client

#     @pytest.fixture
#     def auth_client_2(self):
#         client = APIClient()

#         registration_data = {
#             "email": "test2@example.com",
#             "password": "testpassword",
#         }
#         registration_response = client.post("/api/user/register/", registration_data)
#         assert registration_response.status_code == status.HTTP_201_CREATED

#         login_data = {
#             "email": "test2@example.com",
#             "password": "testpassword",
#         }
#         login_response = client.post("/api/user/login/", login_data)
#         assert login_response.status_code == status.HTTP_200_OK

#         access_token = login_response.data['access_token']
#         client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

#         return client

#     def create_article(self, auth_client_1, title="test_title", content="test_content"):
#         article_data = {
#             "title": title,
#             "content": content,
#         }
#         auth_client_1.post("/api/article/create_article/", article_data)

#     def test_create_empty_article(self, auth_client_1):
#         article_data = {
#             "title": "",
#             "content": "",
#         }
#         response = auth_client_1.post("/api/article/create_article/", article_data)
#         assert response.status_code == status.HTTP_400_BAD_REQUEST

#     def test_create_article_without_authentication(self):
#         article_data = {
#             "title": "aaa",
#             "content": "aaa",
#         }
#         wrong_token = "wrong_token"
#         client = APIClient()
#         response = client.post(
#             "/api/article/create_article/",
#             article_data,
#             HTTP_AUTHORIZATION=f"Bearer {wrong_token}"
#         )
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_update_empty_article(self, auth_client_1):
#         # create article
#         article_data = {
#             "title": "Test Article",
#             "content": "This is a test article.",
#         }
#         response = auth_client_1.post("/api/article/create_article/", article_data)
#         article_id = response.data['id']
#         update_data = {
#             "title": "",
#             "content": "",
#         }
#         response = auth_client_1.patch(f"/api/article/{article_id}/update_article/", update_data)
#         assert response.status_code == status.HTTP_400_BAD_REQUEST

#     def test_update_article_without_authentication(self, auth_client_1):
#         # create article
#         article_data = {
#             "title": "Test Article",
#             "content": "This is a test article.",
#         }
#         response = auth_client_1.post("/api/article/create_article/", article_data)
#         article_id = response.data['id']
#         client = APIClient()
#         wrong_token = "wrong_token"
#         update_data = {
#             "title": "123",
#             "content": "123",
#         }
#         response = client.patch(
#             f"/api/article/{article_id}/update_article/",
#             update_data,
#             HTTP_AUTHORIZATION=f"Bearer {wrong_token}"
#         )
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_update_article_wrong_user(self, auth_client_1, auth_client_2):
#         article_data = {
#             "title": "Test Article",
#             "content": "This is a test article.",
#         }
#         response = auth_client_1.post("/api/article/create_article/", article_data)
#         article_id = response.data['id']
#         update_data = {
#             "title": "123",
#             "content": "123",
#         }
#         update_response = auth_client_2.patch(
#             f"/api/article/{article_id}/update_article/",
#             update_data,
#         )

#         assert update_response.status_code == status.HTTP_403_FORBIDDEN

#     def test_update_nonexistent_article(self, auth_client_1):
#         article_data = {
#             "title": "Test Article",
#             "content": "This is a test article.",
#         }
#         response = auth_client_1.post("/api/article/create_article/", article_data)
#         article_id = response.data['id']
#         auth_client_1.delete(
#             f"/api/article/{article_id}/delete_article/"
#         )
#         delete_response = auth_client_1.delete(
#             f"/api/article/{article_id}/delete_article/"
#         )
#         assert delete_response.status_code == status.HTTP_404_NOT_FOUND

#     def test_delete_article_without_authentication(self, auth_client_1):
#         # create article
#         article_data = {
#             "title": "Test Article",
#             "content": "This is a test article.",
#         }
#         response = auth_client_1.post("/api/article/create_article/", article_data)
#         article_id = response.data['id']
#         client = APIClient()
#         wrong_token = "wrong_token"
#         response = client.delete(
#             f"/api/article/{article_id}/update_article/",
#             HTTP_AUTHORIZATION=f"Bearer {wrong_token}"
#         )
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_delete_article_wrong_user(self, auth_client_1, auth_client_2):
#         article_data = {
#             "title": "Test Article",
#             "content": "This is a test article.",
#         }
#         response = auth_client_1.post("/api/article/create_article/", article_data)
#         article_id = response.data['id']

#         delete_response = auth_client_2.patch(
#             f"/api/article/{article_id}/update_article/",
#         )

#         assert delete_response.status_code == status.HTTP_403_FORBIDDEN

#     def test_delete_nonexistent_article(self, auth_client_1):
#         article_data = {
#             "title": "Test Article",
#             "content": "This is a test article.",
#         }
#         auth_client_1.post("/api/article/create_article/", article_data)
#         nonexistent_article_id = 999999
#         update_data = {
#             "title": "123",
#             "content": "123",
#         }
#         update_response = auth_client_1.patch(
#             f"/api/article/{nonexistent_article_id}/update_article/",
#             update_data,
#         )

#         assert update_response.status_code == status.HTTP_404_NOT_FOUND


# class GetArticleList:

#     @pytest.fixture
#     def article_factory(self, article_factory):
#         def create_article(title, content):
#             return article_factory(title="test_title", content="test_content", author="author")
#         return create_article

#     def test_search_articles_list_with_pagination(self, article_factory):
#         client = APIClient()
#         article_factory("Article 1", "Content 1")
#         article_factory("Article 2", "Content 2")
#         article_factory("Article 3", "Content 3")

#         response = client.get("/api/get_article/")
#         assert response.status_code == status.HTTP_200_OK

#         assert 'results' in response.data
#         assert len(response.data['results']) == 2

#         next_page_url = response.data['next']
#         response = client.get(next_page_url)
#         assert len(response.data['results']) == 1
#         assert 'next' not in response.data

#     def test_retrieve_specific_article(self, article_factory):
#         client = APIClient()
#         article = article_factory("Specific Article", "Specific Content")

#         response = client.get(reverse('get_article', args=[article.id]))
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['title'] == "Specific Article"
#         assert response.data['content'] == "Specific Content"

#         response = client.get(reverse('get_article', args=[article.id + 1]))
#         assert response.status_code == status.HTTP_404_NOT_FOUND
