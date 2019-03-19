from contextlib import contextmanager

from datagen.state import state


def execute(seed, atomic, append, admin_email, superuser_email,
            channel_num, contact_num, broadcast_num, flow_num, archive_num):
    from django.conf import settings
    from datagen import factories
    from datagen.models import orgs
    state.seed = seed

    from django.db import connection
    connection.connect()

    if atomic:
        from django.db.transaction import atomic as _atomic
    else:
        _atomic = contextmanager(lambda: True)

    with _atomic():
        factories.UserFactory(username='superuser', email=admin_email, is_superuser=True, is_staff=True)
        admin = factories.UserFactory(username='admin', email=superuser_email)

        factories.UserFactory(username=settings.ANONYMOUS_USER_NAME)

        for o in orgs.Org.objects.all():
            o.administrators.add(admin)
            factories.ChannelFactory.create_batch(channel_num, org=o)
            factories.ContactFactory.create_batch(contact_num,
                                                  org=o)
            factories.BroadcastFactory.create_batch(broadcast_num,
                                                    org=o)

            factories.FlowFactory.create_batch(flow_num, org=o)
            factories.CampaignFactory.create_batch(10, org=o)
            factories.ArchiveFactory.create_batch(archive_num, org=o)
            factories.LabelFactory.create_batch(70, org=o)
    return True
    # from django.db import connection
    # connection.close()
