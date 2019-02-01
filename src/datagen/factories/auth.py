import factory
from django.conf import settings
from timezone_field import TimeZoneField

import temba.orgs.models as orgs
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from factory import SubFactory
from factory.faker import faker
import temba.locations.models as locations

# @factory.django.mute_signals(post_save)
class UserFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda n: "user-%03d" % n)

    class Meta:
        model = User
        django_get_or_create = ('username',)

