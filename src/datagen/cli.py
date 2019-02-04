import click
import logging
import logging.config

from click import echo

import datagen

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
    logging.config.dictConfig(LOGGING)


@cli.command()
@click.pass_context
def zap(ctx, **kwargs):
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
@click.option('--verbosity', type=int, default=1)
@click.option('-o', '--organization', type=int, default=1)
@click.option('-c', '--channels', type=int, default=1)
@click.pass_context
def db(ctx, organization, channels, verbosity, **kwargs):
    from datagen import factories
    from datagen.models import auth, orgs
    superuser = factories.UserFactory(username='admin',
                                      email='admin@admin.org',
                                      is_superuser=True,
                                      is_staff=True)

    channel = factories.ChannelFactory()
    o = channel.org
    o.administrators.add(superuser)
    for g in o.all_groups.all():
        g.contacts.add(factories.ContactFactory(org=o))

    if verbosity > 2:
        echo('ORGANIZATIONS:')
        for o in orgs.Org.objects.all():
            echo(f'{o.name}')
            echo('  Administrators:')
            for a in o.administrators.all():
                echo(f'    {a.username} {a.email}')

            echo('  Groups:')
            for a in o.all_groups.all():
                echo(f'    {a.name} {a.group_type}')

            echo('  Contacts:')
            for a in o.org_contacts.all():
                echo(f'    {a.name}')
    elif verbosity > 1:
        echo(f'ORGANIZATION: {o}')
        for a in o.administrators.all():
            echo(f'    {a.username} {a.email}')

        echo('  Groups:')
        for a in o.all_groups.all():
            echo(f'    {a.name} {a.group_type}')

        echo('  Contacts:')
        for a in o.org_contacts.all():
            echo(f'    {a.name}')


def main():  # pragma: no cover
    cli(prog_name=datagen.NAME, obj={}, max_content_width=100)
