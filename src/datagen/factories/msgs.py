import factory

from datagen.declarations import RandomRecord
from datagen.factories.common import SmartModelFactory
from datagen.models import channels, contacts, msgs

from .schedules import ScheduleFactory


class BroadcastFactory(SmartModelFactory):
    # org = factory.SubFactory(OrgFactory)
    text = factory.Faker('translatable')
    channel = RandomRecord(channels.Channel.objects)
    # channel = factory.LazyAttribute(lambda o: channels.Channel.objects.order_by('?').first())
    schedule = factory.SubFactory(ScheduleFactory)

    class Meta:
        model = msgs.Broadcast
        django_get_or_create = ('schedule',)

    @factory.post_generation
    def m2m(self, create, extracted, **kwargs):
        self.groups.add(contacts.ContactGroup.all_groups.order_by('?').first())
        # self.groups.add(random.choice(state.groups))
