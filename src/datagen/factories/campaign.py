import factory
from factory import SubFactory

from temba.campaigns.models import Campaign, CampaignEvent

from datagen.factories.common import TembaModelFactory
from datagen.models import contacts


class CampaignFactory(TembaModelFactory):
    group = factory.LazyAttribute(lambda o: contacts.ContactGroup.all_groups.order_by('?').first())

    class Meta:
        model = Campaign


class CampaignEventFactory(TembaModelFactory):
    class Meta:
        model = CampaignEvent

    campaign = SubFactory(CampaignFactory)
