import factory
from django.conf import settings
from timezone_field import TimeZoneField

from ..declarations import Choice
from ..models import contacts, orgs
from .auth import UserFactory
from .common import SmartModelFactory
from .locations import AdminBoundaryFactory


class LanguageFactory(SmartModelFactory):
    class Meta:
        model = orgs.Language


class OrgFactory(SmartModelFactory):
    name = factory.Faker('company')
    language = Choice(settings.LANGUAGES)
    timezone = Choice(TimeZoneField.CHOICES)
    languages = factory.RelatedFactory(LanguageFactory, 'org')
    country = factory.SubFactory(AdminBoundaryFactory)
    slug = factory.LazyAttribute(lambda instance: orgs.Org.get_unique_slug(instance.name))
    brand = settings.DEFAULT_BRAND

    # all_groups = factory.RelatedFactory(ContactGroupFactory,
    #                                     'org')
    #
    # org_contacts = factory.RelatedFactory(ContactFactory,
    #                                     'org')

    class Meta:
        model = orgs.Org
        django_get_or_create = ('name',)

    @factory.post_generation
    def others(self, create, extracted, **kwargs):
        from datagen.factories.contacts import ContactGroupFactory

        if not create:
            return
        self.editors.add(UserFactory())
        self.administrators.add(UserFactory())
        ContactGroupFactory(name="ContactGroup-ALL",
                            group_type=contacts.ContactGroup.TYPE_ALL, org=self)
        ContactGroupFactory(name="ContactGroup-BLOCKED",
                            group_type=contacts.ContactGroup.TYPE_BLOCKED, org=self)
        ContactGroupFactory(name="ContactGroup-STOPPED",
                            group_type=contacts.ContactGroup.TYPE_STOPPED, org=self)
        ContactGroupFactory(group_type=contacts.ContactGroup.TYPE_USER_DEFINED, org=self)
        ContactGroupFactory(group_type=contacts.ContactGroup.TYPE_USER_DEFINED, org=self)
