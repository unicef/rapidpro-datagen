import factory
from factory.faker import faker

from ..models import locations
from ..declarations import LocationName

FAKE = faker.Faker()


class AdminBoundaryFactory(factory.DjangoModelFactory):
    osm_id = factory.Sequence(lambda n: "osm-%03d" % n)
    name = LocationName()

    class Meta:
        model = locations.AdminBoundary
        django_get_or_create = ('osm_id',)
