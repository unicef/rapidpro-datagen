import factory
from django.conf import settings
from timezone_field import TimeZoneField

import temba.orgs.models as orgs
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from factory import SubFactory
from factory.faker import faker
import temba.locations.models as locations
from datagen.declarations import LocationName

FAKE = faker.Faker()


class AdminBoundaryFactory(factory.DjangoModelFactory):
    osm_id = factory.Sequence(lambda n: "osm-%03d" % n)
    name = LocationName()

    class Meta:
        model = locations.AdminBoundary
        django_get_or_create = ('osm_id',)
