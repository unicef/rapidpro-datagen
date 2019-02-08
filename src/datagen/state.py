# -*- coding: utf-8 -*-
from threading import local

from django.utils.functional import cached_property


class State(local):
    contacts = []
    seed = 0


state = State()
