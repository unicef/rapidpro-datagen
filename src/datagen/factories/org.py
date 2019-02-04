import factory
from django.conf import settings
from timezone_field import TimeZoneField

from ..models import orgs, contacts
from ..declarations import Choice
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
    slug = factory.LazyAttribute(lambda o: orgs.Org.get_unique_slug(o.name))
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
        from datagen.factories.contacts import ContactGroupFactory, ContactFactory

        if not create:
            # Simple build, do nothing.
            return

        # self.slug = orgs.Org.get_unique_slug(self.name)
        # self.primary_language = LanguageFactory(org=self)
        self.editors.add(UserFactory())
        self.administrators.add(UserFactory())
        self.viewers.add(UserFactory())
        self.surveyors.add(UserFactory())
        type_all = ContactGroupFactory(group_type=contacts.ContactGroup.TYPE_ALL, org=self)
        type_blocked = ContactGroupFactory(group_type=contacts.ContactGroup.TYPE_BLOCKED, org=self)
        type_stopped = ContactGroupFactory(group_type=contacts.ContactGroup.TYPE_STOPPED, org=self)
        type_ud = ContactGroupFactory(group_type=contacts.ContactGroup.TYPE_USER_DEFINED, org=self)

        # c = ContactFactory(org=self)

        # self.org_contacts.add(c)

        # self.all_groups.add(ContactGroupFactory(group_type=contacts.ContactGroup.TYPE_BLOCKED))
        # self.all_groups.add(ContactGroupFactory(group_type=contacts.ContactGroup.TYPE_STOPPED))
        # self.all_groups.add(ContactGroupFactory(group_type=contacts.ContactGroup.TYPE_USER_DEFINED))
        # self.all_groups.add(ContactGroupFactory(group_type=contacts.ContactGroup.TYPE_ALL,
        #                                         contacts=[c]
        #                                         ))

