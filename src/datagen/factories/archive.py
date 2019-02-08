from datagen.models import archives


import factory

from temba.channels.types import TYPES

from ..declarations import ChannelType, CountryFaker
from ..models import channels
from .common import TembaModelFactory
from .org import OrgFactory


class ArchiveFactory(TembaModelFactory):
    org = factory.SubFactory(OrgFactory)

    class Meta:
        model = archives.Archive
