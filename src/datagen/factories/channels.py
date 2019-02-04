import factory

from datagen.declarations import CountryFaker, ChannelType
from temba.channels.types import TYPES
from .org import OrgFactory
from ..models import channels
from .common import TembaModelFactory


class ChannelFactory(TembaModelFactory):
    country = CountryFaker()
    channel_type = ChannelType()
    name = factory.LazyAttribute(lambda o: TYPES[o.channel_type])
    # address =
    org = factory.SubFactory(OrgFactory)
    # gcm_id =
    # claim_code=
    secret = factory.Faker('password')
    alert_email = factory.Faker('email')

    class Meta:
        model = channels.Channel
