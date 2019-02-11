# -*- coding: utf-8 -*-
from threading import local


class State(local):
    contacts = []
    seed = 0


state = State()
