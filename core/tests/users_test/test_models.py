import pytest
from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db


class TestCustomUserModel:

    # Email address without at
    def test_invalid_email(self, custom_user_factory):
        email = custom_user_factory(email="asdasdasd.com")
        with pytest.raises(ValidationError):
            email.full_clean()

    # if password less than 8
    def test_invalid_password(self, custom_user_factory):
        password = "x" * 7
        obj = custom_user_factory(password=password)
        with pytest.raises(ValidationError):
            obj.full_clean()
