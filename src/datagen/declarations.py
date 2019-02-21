import random

import factory
from django.utils.functional import cached_property
from django_countries import countries
from factory.declarations import OrderedDeclaration


class Choice(factory.Iterator):

    def evaluate(self, instance, step, extra):
        ret = super().evaluate(instance, step, extra)
        return ret[1]


class LocationName(factory.Faker):

    def __init__(self, provider='location_on_land', locale=None, **kwargs):
        super().__init__(provider, locale, **kwargs)

    def evaluate(self, instance, step, extra):
        ret = super().evaluate(instance, step, extra)
        return ret[2]


class CountryFaker(OrderedDeclaration):

    def evaluate(self, instance, step, extra):
        return random.choice(countries)[0]


class RandomRecord(OrderedDeclaration):

    def __init__(self, queryset) -> None:
        self.queryset = queryset
        # super().__init__(**kwargs)

    @cached_property
    def data(self):
        return self.queryset.all()

    def evaluate(self, instance, step, extra):
        return random.choice(self.data)


class ChannelType(OrderedDeclaration):

    def __init__(self, **kwargs):
        from temba.channels.types import TYPES
        super().__init__(**kwargs)
        self.choices = list(TYPES.keys())

    def evaluate(self, instance, step, extra):
        return random.choice(self.choices)


class RandomUser(RandomRecord):

    def __init__(self, **kwargs):
        from django.contrib.auth.models import User
        super().__init__(User.objects)
