import uuid

import factory

from datagen.declarations import RandomUser
from datagen.state import state


class SmartModelFactory(factory.DjangoModelFactory):
    created_by = RandomUser()
    modified_by = RandomUser()

    class Meta:
        abstract = True


class TembaModelFactory(SmartModelFactory):
    uuid = factory.Sequence(lambda n: uuid.uuid4())

    class Meta:
        abstract = True


class SquashableModelFactory(SmartModelFactory):
    uuid = factory.Sequence(lambda n: uuid.uuid4())

    class Meta:
        abstract = True
