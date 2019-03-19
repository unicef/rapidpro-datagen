import factory

from datagen.state import state
from datagen.declarations import RandomUser
from datagen.factories import ChannelSessionFactory

from ..models import msgs
from .common import SmartModelFactory, SquashableModelFactory, TembaModelFactory
from .org import OrgFactory


class LabelFactory(TembaModelFactory):
    id = factory.Sequence(lambda n:  state.seed + n)

    org = factory.SubFactory(OrgFactory)
    name = factory.Sequence(lambda o: "Label-%d" % (state.seed + o))

    class Meta:
        model = msgs.Label
