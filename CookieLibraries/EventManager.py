# coding: utf-8

# Created by BigCookie233

import inspect

event_listeners = {}


class Event:
    def call(self):
        if self.__class__ in event_listeners:
            for listener in event_listeners[self.__class__]:
                listener(self)


def event_listener(*args, **kwargs):
    if args[0] is None:
        raise TypeError("missing 1 required argument")
    if not issubclass(args[0], Event):
        raise TypeError("incorrect argument")

    def wrapper(func):
        if len(inspect.signature(func).parameters) != 1:
            raise TypeError("The listener takes 0 positional arguments but 1 will be given")
        event_listeners.setdefault(args[0], []).append(func)

    return wrapper
