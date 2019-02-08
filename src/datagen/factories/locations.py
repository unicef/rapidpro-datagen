import factory
from factory.faker import faker

from ..declarations import LocationName
from ..models import locations

FAKE = faker.Faker()


class AdminBoundaryFactory(factory.DjangoModelFactory):
    osm_id = factory.Sequence(lambda n: "osm-%03d" % n)
    name = LocationName()

    class Meta:
        model = locations.AdminBoundary
        django_get_or_create = ('osm_id',)
