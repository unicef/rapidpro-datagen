import sys
from functools import partial

import click


def secho(*args, fg='white'):
    click.secho(" ".join(map(str, args)), fg=fg)


def fail(*args):
    secho(*args, fg='red')
    sys.exit(1)


echo = partial(secho, fg='white')
success = partial(secho, fg='green')
warn = partial(secho, fg='yellow')
error = partial(secho, fg='red')
