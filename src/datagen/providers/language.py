import factory
from faker.providers import BaseProvider


class OceanProvider(BaseProvider):
    __provider__ = "ocean"
    __lang__ = "en_US"
    oceans = [
        u'Atlantic', u'Pacific', u'Indian', u'Arctic', u'Southern',
    ]

    @classmethod
    def ocean(cls):
        return cls.random_element(cls.oceans)


factory.Faker.add_provider(OceanProvider)
