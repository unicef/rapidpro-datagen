import uuid

import factory

from datagen.factories import ChannelFactory
from temba.channels.types import TYPES

from ..declarations import ChannelType, CountryFaker
from ..models import channels
from .common import TembaModelFactory
from .org import OrgFactory



class ChannelEventFactory(TembaModelFactory):
    channel = factory.SubFactory(ChannelFactory)

    class Meta:
        model = channels.ChannelEvent
        django_get_or_create = ('org', 'channel_type')
