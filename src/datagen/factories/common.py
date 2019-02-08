import uuid

import factory
from django.contrib.auth.models import User

from datagen.declarations import RandomRecord
from .auth import UserFactory


class SmartModelFactory(factory.DjangoModelFactory):
    created_by = RandomRecord(User.objects)
    modified_by = RandomRecord(User.objects)

    class Meta:
        abstract = True


class TembaModelFactory(SmartModelFactory):
    uuid = factory.Sequence(lambda n: uuid.uuid4())

    class Meta:
        abstract = True
