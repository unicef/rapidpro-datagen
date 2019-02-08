import random

import factory
import factory.fuzzy
from factory import random
from datagen.declarations import RandomRecord
from datagen.factories.common import SmartModelFactory
from datagen.models import channels, contacts, msgs
from datagen.state import state

from .schedules import ScheduleFactory


class BroadcastFactory(SmartModelFactory):
    # org = factory.SubFactory(OrgFactory)
    # id = factory.fuzzy.FuzzyInteger(state.seed)

    # id = factory.LazyAttribute(lambda o: random.randgen.randrange(state.seed, state.seed 1, 1))
    id = factory.Sequence(lambda n: state.seed + n)
    text = factory.Faker('translatable')
    channel = RandomRecord(channels.Channel.objects)
    # channel = factory.LazyAttribute(lambda o: channels.Channel.objects.order_by('?').first())
    # channel = factory.LazyAttribute(lambda o: channels.Channel.objects.order_by('?').first())
    # schedule = factory.SubFactory(ScheduleFactory)
    schedule = factory.LazyAttribute(lambda o: ScheduleFactory(id=o.id))

    class Meta:
        model = msgs.Broadcast
        django_get_or_create = ('id',)

    @factory.post_generation
    def m2m(self, create, extracted, **kwargs):
        self.groups.add(contacts.ContactGroup.all_groups.order_by('?').first())
        # self.groups.add(random.choice(state.groups))
