import random

import factory

from datagen.factories.common import SmartModelFactory
from datagen.models import schedules


class ScheduleFactory(SmartModelFactory):
    status = factory.LazyAttribute(lambda instance: random.choice(schedules.Schedule.STATUS_CHOICES)[0])
    repeat_period = factory.LazyAttribute(lambda instance: random.choice(schedules.Schedule.REPEAT_CHOICES)[0])

    id = factory.Sequence(lambda n: n + 1)

    class Meta:
        model = schedules.Schedule
        django_get_or_create = ('id',)
