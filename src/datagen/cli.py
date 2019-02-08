import random
from contextlib import contextmanager
from time import time

import click
from click import echo
from django.db.models import Max

import datagen
from datagen.state import state

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {"level": "WARNING", "handlers": ["console"]},
    "formatters": {"verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"}},
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "verbose"},
        "null": {"class": "logging.NullHandler"},
    },
    "loggers": {
        "pycountry": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {"handlers": ["null"], "propagate": False},
        "django.db.backends": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        # "": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
        "django": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "temba": {"level": "ERROR", "handlers": ["console"], "propagate": False},
    },
}


@click.group()
@click.version_option(version=datagen.VERSION)
@click.pass_context
def cli(ctx, **kwargs):
    import django
    django.setup()


@cli.command('zap')
@click.pass_context
def erase_all(ctx, **kwargs):
    from .models import orgs, locations, auth, channels
    from django.db import connections

    models = [orgs.Language, orgs.Org, locations.AdminBoundary, auth.User, channels.Channel]
    conn = connections['default']
    cursor = conn.cursor()
    cursor.execute("SET session_replication_role TO 'replica'")

    for model in models:
        click.echo(f"Truncating {model._meta.verbose_name} ({model._meta.db_table})")
        cursor.execute(f'TRUNCATE TABLE "{model._meta.db_table}" RESTART IDENTITY CASCADE')

    cursor.execute("SET session_replication_role TO 'origin'")


@cli.command()
@click.option('-v', '--verbosity', type=int, default=1)
@click.option('--zap', is_flag=True, help="Erase all data first")
@click.option('--atomic', is_flag=True, envvar='ATOMIC_TRANSACTIONS', help="Use single transaction")
@click.option('--append', is_flag=True)
@click.option('--profile', type=click.File())
@click.option('--seed', type=int, default=1)
@click.option('--organizations', type=int, default=1, help='Number od Organizations to create')
@click.option('--channels', 'channel_num', type=int, default=1, help='Minimum number of Channels to create')
@click.option('--contacts', 'contact_num', type=int, default=1, help='Minimum number of Contacts to create')
@click.option('--archives', 'archive_num', type=int, default=1, help='Minimum number of Archive to create')
@click.option('--flows', 'flow_num', type=int, default=1, help='Minimum number of Flow to create')
@click.option('--broadcasts', type=int, default=100, help='Minimum number of Broadcasts to create')
@click.option('--base-email',
              metavar='EMAIL',
              envvar='BASE_EMAIL',
              help='Base GMail addres to use for email generation')
@click.option('--admin-email',
              metavar='EMAIL',
              envvar='ADMIN_EMAIL',
              default='admin@admin.org',
              help='Alll Organizanizations admin\'s email')
@click.option('--superuser-email',
              metavar='EMAIL',
              envvar='SUPERUSER_EMAIL',
              default='superuser@superuser.org',
              help='System superuser email')
@click.pass_context
def db(ctx, organizations, channel_num, contact_num, archive_num, broadcasts, flow_num,
       verbosity, zap, atomic, base_email, append, seed,
       admin_email, superuser_email, **kwargs):
    from datagen import factories
    from datagen.models import orgs, auth, msgs
    from django.conf import settings
    import datagen.providers  # noqa
    if zap:
        ctx.invoke(erase_all)
    if atomic:
        from django.db.transaction import atomic as _atomic
    else:
        _atomic = contextmanager(lambda: True)

    start = time()
    if append:
        state.seed = 1 + msgs.Broadcast.objects.all().aggregate(seed=Max('id'))['seed']
    else:
        state.seed = seed

    with _atomic():
        factories.UserFactory(username='superuser',
                              email=admin_email,
                              is_superuser=True,
                              is_staff=True)

        admin = factories.UserFactory(username='admin',
                                      email=superuser_email,
                                      is_superuser=False,
                                      is_staff=False)

        factories.UserFactory(username=settings.ANONYMOUS_USER_NAME)
        if not append:
            factories.UserFactory.create_batch(100)
            factories.OrgFactory.create_batch(organizations)
            echo(f'Created #{organizations} Organizations')

        for o in orgs.Org.objects.all():
            o.administrators.add(admin)
            factories.ChannelFactory.create_batch(channel_num, org=o)
            factories.ContactFactory.create_batch(contact_num,
                                                  org=o)
            factories.BroadcastFactory.create_batch(broadcasts,
                                                    org=o)

            factories.FlowFactory.create_batch(flow_num,
                                               org=o)
            # factories.ArchiveFactory.create_batch(archive_num,
            #                                       org=o)

    stop = time()
    duration = stop - start
    click.echo("Execution time: %.3f secs" % duration)

    if verbosity > 1:
        echo('seed: %s' % state.seed)
        echo('Users: %s' % auth.User.objects.count())
        echo('Organizations: %s' % orgs.Org.objects.count())
        for o in orgs.Org.objects.all():
            echo(f'Organization: "{o.name}"')
            echo('  Administrators: %s' % o.administrators.count())
            echo('  Groups: %s' % o.all_groups.count())
            echo('  Contacts: %s' % o.org_contacts.count())
            echo('  Broadcasts: %s' % o.broadcast_set.count())
            echo('  Flows: %s' % o.flows.count())


def main():  # pragma: no cover
    cli(prog_name=datagen.NAME, obj={}, max_content_width=100)
