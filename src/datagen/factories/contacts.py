import factory

# from datagen.factories import OrgFactory
from datagen.factories.common import TembaModelFactory

from ..models import channels, contacts


class ContactGroupFactory(TembaModelFactory):
    name = factory.Sequence(lambda o: "ContactGroup-%s" % o)
    group_type = contacts.ContactGroup.TYPE_ALL
    status = contacts.ContactGroup.STATUS_READY
    # org = factory.SubFactory(OrgFactory)

    class Meta:
        model = contacts.ContactGroup
        django_get_or_create = ('org', 'name',)


class ContactFactory(TembaModelFactory):
    # name = factory.Sequence(lambda instance: "Contact-%s" % instance)
    name = factory.Faker('name')
    # org = factory.SubFactory(OrgFactory)
    is_blocked = False
    is_test = False

    class Meta:
        model = contacts.Contact
        django_get_or_create = ('org', 'name',)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """Save again the instance if creating and at least one hook ran."""
        if create and results:
            # Some post-generation hooks ran, and may have modified us.
            instance.save(update_fields=None, handle_update=False)

    @factory.post_generation
    def m2m(self, create, extracted, **kwargs):
        if not create:
            return
        ContactURNFactory(contact=self, org=self.org)


class ContactURNFactory(factory.DjangoModelFactory):
    contact = factory.SubFactory(ContactFactory)
    # org = factory.SubFactory(OrgFactory)
    channel = factory.LazyAttribute(
        lambda o: channels.Channel.objects.order_by('?').first())

    priority = contacts.ContactURN.PRIORITY_STANDARD
    scheme = 'mailto'
    path = factory.Faker('email')
    identity = factory.LazyAttribute(lambda o: 'mailto:%s' % o.path)

    class Meta:
        model = contacts.ContactURN
        django_get_or_create = ('identity',)
