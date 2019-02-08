import random

import factory

from datagen.factories.common import SmartModelFactory
from .schedules import ScheduleFactory
from datagen.models import msgs, channels, contacts


class BroadcastFactory(SmartModelFactory):
    # org = factory.SubFactory(OrgFactory)
    text = factory.Faker('translatable')
    channel = factory.LazyAttribute( lambda o: channels.Channel.objects.order_by('?').first())
    schedule = factory.SubFactory(ScheduleFactory)

    class Meta:
        model = msgs.Broadcast
        django_get_or_create = ('schedule',)

    @factory.post_generation
    def m2m(self, create, extracted, **kwargs):
        self.groups.add(contacts.ContactGroup.all_groups.order_by('?').first())
        # self.groups.add(random.choice(state.groups))
