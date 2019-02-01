import factory


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
