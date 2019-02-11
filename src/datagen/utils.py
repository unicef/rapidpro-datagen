import datetime
from contextlib import contextmanager

from django.db import connection
from pytz import reference

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def permute_email(*emails):
    for base in emails:
        address, domain = base.split('@')
        for i in range(1, len(address)):
            a = list(address)
            a.insert(i, '.')
            yield f'{"".join(a)}@{domain}'


@contextmanager
def disable_triggers():
    with connection.cursor() as cursor:
        cursor.execute("SET session_replication_role TO 'replica';")
    yield
    with connection.cursor() as cursor:
        cursor.execute("SET session_replication_role TO 'origin'")


def delta(s):
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    if int(seconds) == 0:
        return '{:02}:{:02}:{:02}.{:06}'.format(int(hours), int(minutes), int(seconds), int(remainder))
    else:
        return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))


def now():
    d = datetime.datetime.now()
    return d.astimezone(reference.LocalTimezone()).strftime(DATE_FORMAT)
