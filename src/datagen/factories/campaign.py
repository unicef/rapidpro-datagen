from factory import SubFactory

from temba.campaigns.models import Campaign, CampaignEvent

from datagen.factories.common import TembaModelFactory


class CampaignFactory(TembaModelFactory):
    class Meta:
        model = Campaign


class CampaignEventFactory(TembaModelFactory):
    class Meta:
        model = CampaignEvent

    campaign = SubFactory(CampaignFactory)
