import math
import multiprocessing
import os
from time import time

import click

import datagen

from .generator import execute
from .out import echo, warn
from .utils import delta, now

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
    echo('Database: %s' % os.environ['DATABASE_URL'])
    import django
    django.setup()


@cli.command()
@click.pass_context
def status(ctx, **kwargs):
    """display database numbers """
    from datagen.models import orgs, auth, msgs

    from datagen.state import state
    echo('Seed: %s' % state.seed)
    echo('')
    echo('Users: %s' % auth.User.objects.count())
    echo('Organizations: %s' % orgs.Org.objects.count())
    for o in orgs.Org.objects.all():
        echo(f'Organization: "{o.name}"')
        echo('  Administrators: %s' % o.administrators.count())
        echo('  Groups: %s' % o.all_groups.count())
        echo('  Contacts: %s' % o.org_contacts.count())
        echo('  Broadcasts: %s' % o.broadcast_set.count())
        echo('  Flows: %s' % o.flows.count())


@cli.command('zap')
@click.pass_context
def erase_all(ctx, **kwargs):
    """ empty database """
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
@click.option('--atomic', is_flag=True, envvar='ATOMIC_TRANSACTIONS',
              help="Use single transaction. Do not use for large dataset  (>~500.000")
@click.option('--create/--append', is_flag=True,
              help="Create new organizations or append new data to existing")
@click.option('-p', '--processes', type=int, default=int(multiprocessing.cpu_count() / 2),
              help="number of processes to use")
@click.option('--seed', type=int, default=1, help="initial pk value for numbers")
# Config
@click.option('--base-email', metavar='EMAIL', envvar='BASE_EMAIL',
              help='Base GMail addres to use for email generation')
@click.option('--admin-email', metavar='EMAIL', envvar='ADMIN_EMAIL', default='admin@admin.org',
              help='Alll Organizanizations admin\'s email')
@click.option('--superuser-email', metavar='EMAIL', envvar='SUPERUSER_EMAIL', default='superuser@superuser.org',
              help='System superuser email')
# Numbers
@click.option('--users', 'user_num', type=int, default=100,
              help='Number od Users to create')
@click.option('--organizations', type=int, default=1,
              help='Number od Organizations to create')
@click.option('--channels', 'channel_num', type=int, default=1,
              help='Minimum number of Channels to create')
@click.option('--contacts', 'contact_num', type=int, default=1000,
              help='Minimum number of Contacts to create')
@click.option('--archives', 'archive_num', type=int, default=1,
              help='Minimum number of Archive to create')
@click.option('--flows', 'flow_num', type=int, default=100,
              help='Minimum number of Flow to create')
@click.option('--broadcasts', 'broadcast_num', type=int, default=1000,
              help='Minimum number of Broadcasts to create')
@click.option('--archives', type=int, default=10,
              help='Minimum number of Archives to create')
@click.pass_context
def db(ctx, organizations, user_num, channel_num, contact_num, archive_num, broadcast_num, flow_num,
       verbosity, zap, atomic, base_email, create, seed, processes,
       admin_email, superuser_email, **kwargs):
    """ generate data """
    from datagen.models import msgs
    from datagen import factories
    from django.db.models import Max

    append = not create
    if zap:
        ctx.invoke(erase_all)

    start = time()
    if append:
        try:
            seed = 1 + msgs.Broadcast.objects.all().aggregate(seed=Max('id'))['seed']
        except TypeError:
            warn("No existing data. Ignoring '--append' flag")
            append = False

    echo("Start loading at %s " % now())

    if not append:
        echo(f"Creating #{user_num} Users")
        factories.UserFactory.create_batch(user_num)
        echo(f"Creating #{organizations} Organizations")
        factories.OrgFactory.create_batch(organizations)

    echo(f"Creating: #{channel_num} Channels, #{contact_num} contacts, "
         f"#{broadcast_num} broadcast, #{flow_num} flows, #{archive_num} archives")
    echo("Processes #%s " % processes)
    if processes > 1:
        numbers = list(map(lambda x: math.ceil(x / processes), [channel_num, contact_num,
                                                                 broadcast_num, flow_num,
                                                                 archive_num]))

        args = []
        for p in range(processes):
            args.append([((p+seed)*broadcast_num), atomic,
                         append, admin_email, superuser_email] + numbers)
        with multiprocessing.Pool(processes) as pool:
            out = pool.starmap(execute, args)
            echo(out)
    else:
        execute(seed, atomic, append, admin_email, superuser_email,
                channel_num, contact_num, broadcast_num, flow_num, archive_num)

    stop = time()
    duration = stop - start
    echo("End loading at %s " % now())
    echo("Execution time: %s" % delta(duration))

    if verbosity > 1:
        from django.db import connection
        connection.connect()
        ctx.invoke(status)


def main():  # pragma: no cover
    cli(prog_name=datagen.NAME, obj={}, max_content_width=100)
