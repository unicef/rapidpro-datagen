import factory

from .auth import UserFactory


class SmartModelFactory(factory.DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)

    class Meta:
        abstract = True

