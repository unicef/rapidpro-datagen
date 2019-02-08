from datagen.factories import ChannelSessionFactory
from datagen.models import archives

import factory

from temba.channels.types import TYPES

from ..declarations import ChannelType, CountryFaker
from ..models import flows
from .common import TembaModelFactory
from .org import OrgFactory


class FlowSessionFactory(TembaModelFactory):
    class Meta:
        model = flows.FlowSession


class FlowRunFactory(TembaModelFactory):
    org = factory.SubFactory(OrgFactory)
    session = factory.SubFactory(FlowSessionFactory)
    connection = factory.SubFactory(ChannelSessionFactory)

    class Meta:
        model = flows.FlowRun
