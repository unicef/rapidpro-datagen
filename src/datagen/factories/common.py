import uuid

import factory

from .auth import UserFactory


class SmartModelFactory(factory.DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)

    class Meta:
        abstract = True


class TembaModelFactory(SmartModelFactory):
    uuid = factory.Sequence(lambda n: uuid.uuid4())

    class Meta:
        abstract = True
