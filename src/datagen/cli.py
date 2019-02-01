import click

import datagen


@click.group()
@click.version_option(version=datagen.VERSION)
@click.pass_context
def cli(ctx, **kwargs):
    import django
    django.setup()
    from django.conf import settings


@cli.command()
@click.pass_context
def db(ctx, **kwargs):
    from datagen import factories
    factories.OrgFactory()


def main():  # pragma: no cover
    cli(prog_name=datagen.NAME, obj={}, max_content_width=100)
