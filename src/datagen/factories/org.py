import factory
import temba.orgs.models as orgs
from django.conf import settings
from factory.faker import faker
from timezone_field import TimeZoneField

from datagen.declarations import Choice
from .auth import UserFactory
from .locations import AdminBoundaryFactory
from .common import SmartModelFactory


class LanguageFactory(SmartModelFactory):
    # org = factory.SubFactory(OrgFactory)
    class Meta:
        model = orgs.Language
        # django_get_or_create = ('iso_code',)
    #
    # @factory.post_generation
    # def others(self, create, extracted, **kwargs):
    #     picked = random.choice(settings.LANGUAGES)
    #     if not create:
    #         # Simple build, do nothing.
    #         return

class OrgFactory(SmartModelFactory):
    name = factory.Faker('company')
    language = Choice(settings.LANGUAGES)
    timezone = Choice(TimeZoneField.CHOICES)
    languages = factory.RelatedFactory(LanguageFactory, 'org')
    country = factory.SubFactory(AdminBoundaryFactory)

    class Meta:
        model = orgs.Org
        django_get_or_create = ('name',)

    @factory.post_generation
    def others(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        self.slug = orgs.Org.get_unique_slug(self.name)
        # self.primary_language = LanguageFactory(org=self)
        self.editors.add(UserFactory())
        self.administrators.add(UserFactory())
        self.viewers.add(UserFactory())
        self.surveyors.add(UserFactory())
