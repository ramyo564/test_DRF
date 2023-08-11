import factory
from users.models import CustomUser
from articles.models import Article


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = "password"

    is_active = True
    is_admin = False
    is_staff = False
    is_superuser = False


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.Sequence(lambda n: "test_article_name_%d" % n)
    content = factory.Faker('paragraph', nb_sentences=3)
    author = factory.SubFactory(CustomUserFactory)
