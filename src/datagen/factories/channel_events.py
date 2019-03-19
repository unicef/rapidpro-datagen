import factory

from datagen.factories import ChannelFactory

from ..models import channels
from .common import TembaModelFactory


class ChannelEventFactory(TembaModelFactory):
    channel = factory.SubFactory(ChannelFactory)

    class Meta:
        model = channels.ChannelEvent
        django_get_or_create = ('org', 'channel_type')
