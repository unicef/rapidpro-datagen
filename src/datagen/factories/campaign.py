from factory import SubFactory

from datagen.factories.common import TembaModelFactory
from temba.campaigns.models import Campaign, CampaignEvent


class CampaignFactory(TembaModelFactory):
    class Meta:
        model = Campaign


class CampaignEventFactory(TembaModelFactory):
    class Meta:
        model = CampaignEvent

    campaign = SubFactory(CampaignFactory)
