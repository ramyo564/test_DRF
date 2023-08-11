import pytest

pytestmark = pytest.mark.django_db


class TestArticleModel:
    def test_article(self, article_factory, custom_user_factory):
        author = custom_user_factory()
        obj = article_factory(title="test_title", content="test_content", author=author)

        assert obj.title == "test_title"
        assert obj.content == "test_content"
        assert obj.author == author
