import factory

from temba.channels.types import TYPES

from ..declarations import ChannelType, CountryFaker
from ..models import channels
from .common import TembaModelFactory
from .org import OrgFactory


class ChannelFactory(TembaModelFactory):
    country = CountryFaker()
    channel_type = ChannelType()
    name = factory.LazyAttribute(lambda instance: TYPES[instance.channel_type])
    # address =
    org = factory.SubFactory(OrgFactory)
    # gcm_id =
    # claim_code=
    secret = factory.Faker('password')
    alert_email = factory.Faker('email')

    class Meta:
        model = channels.Channel
        django_get_or_create = ('org', 'channel_type')
