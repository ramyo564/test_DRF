import factory
from users.models import CustomUser
from articles.models import Article
from faker import Faker


fake = Faker()


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Sequence(lambda n: f'user_{n}@example.com')
    password = factory.LazyAttribute(lambda _: fake.pystr(min_chars=8, max_chars=128))

    is_active = True
    is_admin = False
    is_staff = False
    is_superuser = False


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.Faker('sentence')
    content = factory.Faker('paragraph', nb_sentences=3)
    author = factory.SubFactory(CustomUserFactory)
