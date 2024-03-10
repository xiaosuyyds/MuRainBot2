# coding: utf-8

# Created by BigCookie233

import inspect

event_listeners = {}


class Event:
    def call(self):
        if self.__class__ in event_listeners:
            for listener in event_listeners[self.__class__]:
                listener(self)


def event_listener(event_class):
    if event_class is None:
        raise TypeError("missing 1 required argument")
    if not issubclass(event_class, Event):
        raise TypeError("incorrect argument")

    def wrapper(func):
        if len(inspect.signature(func).parameters) != 1:
            raise TypeError("The listener takes 0 positional arguments but 1 will be given")
        event_listeners.setdefault(event_class, []).append(func)
        return func

    return wrapper
