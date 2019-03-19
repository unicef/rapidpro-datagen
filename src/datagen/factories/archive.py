import datetime

import factory
from factory.fuzzy import FuzzyDate, FuzzyDateTime, FuzzyInteger

from datagen.models import archives


class ArchiveFactory(factory.DjangoModelFactory):
    # org = factory.SubFactory(OrgFactory)
    start_date = FuzzyDate(datetime.date(2008, 1, 1))
    build_time = FuzzyInteger(0, 99999)
    rollup = None

    class Meta:
        model = archives.Archive
