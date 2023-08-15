import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import (
       CustomUserFactory,
       ArticleFactory,
       SuperUserFactory,
       TokenFactory,
)
register(CustomUserFactory)
register(SuperUserFactory)
register(ArticleFactory)
register(TokenFactory)


@pytest.fixture
def api_client():
    return APIClient
