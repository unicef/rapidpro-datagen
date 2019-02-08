import factory

from datagen.declarations import RandomUser
from datagen.factories import ChannelSessionFactory

from ..models import flows
from .common import SmartModelFactory, SquashableModelFactory, TembaModelFactory
from .org import OrgFactory


class FlowSessionFactory(factory.DjangoModelFactory):
    class Meta:
        model = flows.FlowSession


class FlowFactory(TembaModelFactory):
    org = factory.SubFactory(OrgFactory)
    saved_by = RandomUser()

    class Meta:
        model = flows.Flow

    @factory.post_generation
    def m2m(self, create, extracted, **kwargs):
        pass
        # flow_dependencies -> Flow
        # group_dependencies -> ContactGroup
        # field_dependencies -> field_dependencies



class FlowRunFactory(factory.DjangoModelFactory):
    org = factory.SubFactory(OrgFactory)
    session = factory.SubFactory(FlowSessionFactory)
    connection = factory.SubFactory(ChannelSessionFactory)

    class Meta:
        model = flows.FlowRun


class RuleSetFactory(factory.DjangoModelFactory):
    class Meta:
        model = flows.RuleSet


class ActionSetFactory(factory.DjangoModelFactory):
    class Meta:
        model = flows.ActionSet


class FlowRevisionFactory(SmartModelFactory):
    class Meta:
        model = flows.FlowRevision


class FlowCategoryCountFactory(SquashableModelFactory):
    class Meta:
        model = flows.FlowCategoryCount


class FlowPathCountFactory(SquashableModelFactory):
    class Meta:
        model = flows.FlowPathCount


class FlowPathRecentRunFactory(factory.DjangoModelFactory):
    class Meta:
        model = flows.FlowPathRecentRun


class FlowNodeCountFactory(SquashableModelFactory):
    class Meta:
        model = flows.FlowNodeCount


class FlowRunCountFactory(SquashableModelFactory):
    class Meta:
        model = flows.FlowRunCount


class ExportFlowResultsTaskFactory(TembaModelFactory):
    class Meta:
        model = flows.ExportFlowResultsTask


class ActionLogFactory(factory.DjangoModelFactory):
    class Meta:
        model = flows.ActionLog


class FlowStartFactory(SmartModelFactory):
    class Meta:
        model = flows.FlowStart


class FlowStartCountFactory(SquashableModelFactory):
    class Meta:
        model = flows.FlowStartCount


class FlowLabelFactory(factory.DjangoModelFactory):
    class Meta:
        model = flows.FlowLabel
