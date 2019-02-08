# -*- coding: utf-8 -*-
from threading import local


class State(local):
    contacts = []


state = State()
