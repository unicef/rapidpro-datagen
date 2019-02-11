import factory

from ..models import auth


# @factory.django.mute_signals(post_save)
class UserFactory(factory.DjangoModelFactory):
    username = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', '123')
    is_superuser = False
    is_staff = False

    class Meta:
        model = auth.User
        django_get_or_create = ('username',)
