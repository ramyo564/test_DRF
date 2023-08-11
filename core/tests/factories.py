import factory
from users.models import CustomUser


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
