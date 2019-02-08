import factory
from faker import Faker
from faker.providers import BaseProvider

fake = Faker()


class TranslatableProvider(BaseProvider):
    __provider__ = "translatable"
    __lang__ = "en_US"

    @classmethod
    def translatable(cls):
        return {'en': fake.sentence()
                }


factory.Faker.add_provider(TranslatableProvider)
