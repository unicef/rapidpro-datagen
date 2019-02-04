import random

import factory
from django_countries import countries
from factory.declarations import OrderedDeclaration


class Choice(factory.Iterator):

    def evaluate(self, sequence, obj, create, extra=None, containers=()):
        ret = super().evaluate(sequence, obj, create, extra, containers)
        return ret[1]


class LocationName(factory.Faker):

    def __init__(self, provider='location_on_land', locale=None, **kwargs):
        super().__init__(provider, locale, **kwargs)

    def evaluate(self, sequence, obj, create, extra=None, containers=()):
        ret = super().evaluate(sequence, obj, create, extra, containers)
        return ret[2]


class CountryFaker(OrderedDeclaration):

    def evaluate(self, sequence, obj, create, extra=None, containers=()):
        return random.choice(countries)[0]


class RandomRecord(OrderedDeclaration):

    def __init__(self, queryset) -> None:
        self.queryset = queryset

    def evaluate(self, sequence, obj, create, extra=None, containers=()):
        return random.choice(self.queryset.all())


class ChannelType(OrderedDeclaration):

    def __init__(self) -> None:
        from temba.channels.types import TYPES
        self.choices = list(TYPES.keys())

    def evaluate(self, sequence, obj, create, extra=None, containers=()):
        return random.choice(self.choices)
