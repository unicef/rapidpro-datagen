import factory
from faker.providers import BaseProvider

from faker import Faker

fake = Faker()


class TranslatableProvider(BaseProvider):
    __provider__ = "translatable"
    __lang__ = "en_US"

    @classmethod
    def translatable(cls):
        return {'en': fake.sentence()
                }


factory.Faker.add_provider(TranslatableProvider)
