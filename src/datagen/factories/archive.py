import factory

from datagen.models import archives

from .common import TembaModelFactory
from .org import OrgFactory


class ArchiveFactory(TembaModelFactory):
    org = factory.SubFactory(OrgFactory)

    class Meta:
        model = archives.Archive
