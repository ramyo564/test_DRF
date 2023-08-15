import factory
from users.models import CustomUser, CustomUserManager
from articles.models import Article
from rest_framework.authtoken.models import Token
from faker import Faker


fake = Faker()


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f'user_{n}@example.com')
    password = factory.LazyAttribute(lambda _: fake.pystr(min_chars=8, max_chars=128))

    is_active = True
    is_admin = False
    is_staff = False
    is_superuser = False


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUserManager

    email = factory.Sequence(lambda n: f'user_{n}@example.com')
    password = factory.LazyAttribute(lambda _: fake.pystr(min_chars=8, max_chars=128))


class TokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Token

    user = factory.SubFactory(CustomUserFactory)


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.Faker('sentence')
    content = factory.Faker('paragraph', nb_sentences=3)
    author = factory.SubFactory(CustomUserFactory)
