import datetime

import factory
from factory.fuzzy import FuzzyDate, FuzzyDateTime

from datagen.models import archives

from .org import OrgFactory


class ArchiveFactory(factory.DjangoModelFactory):
    # org = factory.SubFactory(OrgFactory)
    start_date = FuzzyDate(datetime.date(2008, 1, 1))
    build_time = FuzzyDateTime(datetime.datetime.now(tz=datetime.timezone.utc))
    rollup = None

    class Meta:
        model = archives.Archive
