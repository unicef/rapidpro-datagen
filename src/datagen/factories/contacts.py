import factory

from datagen.factories import OrgFactory, ChannelFactory
from datagen.factories.common import TembaModelFactory
from datagen.models import contacts


class ContactGroupFactory(TembaModelFactory):
    name = factory.Sequence(lambda o: "ContactGroup-%s" % o)
    group_type = contacts.ContactGroup.TYPE_ALL
    status = contacts.ContactGroup.STATUS_READY
    org = factory.SubFactory(OrgFactory)

    class Meta:
        model = contacts.ContactGroup
        django_get_or_create = ('org', 'name',)

    @factory.post_generation
    def others(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        # contacts = extracted.pop('contacts', None)
        # TODO: remove me
        # print(111, "contacts.py:24", 11111, contacts)


class ContactFactory(TembaModelFactory):
    name = factory.Sequence(lambda o: "Contact-%s" % o)
    org = factory.SubFactory(OrgFactory)

    is_blocked = False
    is_test = False

    class Meta:
        model = contacts.Contact
        django_get_or_create = ('org', 'name',)


class ContactURNFactory(factory.DjangoModelFactory):
    contact = factory.SubFactory(ContactFactory)
    org = factory.SubFactory(OrgFactory)
    channel = factory.SubFactory(ChannelFactory)
    priority = contacts.ContactURN.PRIORITY_STANDARD

    class Meta:
        model = contacts.ContactURN
        django_get_or_create = ('identity',)
