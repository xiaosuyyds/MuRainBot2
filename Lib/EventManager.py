# coding: utf-8

# Created by BigCookie233

import inspect
from enum import Enum

import Lib.LoggerManager as LoggerManager

event_listeners = {}


class Priority(Enum):
    HIGHEST = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    LOWEST = 4


class Event:
    def call(self):
        for module in event_listeners.values():
            if self.__class__ in module:
                for priority in sorted(module[self.__class__].keys(), key=lambda x: x.value):
                    for listener in module[self.__class__][priority]:
                        LoggerManager.log_exception(True)(listener)(self)


class CancellableEvent(Event):
    def __init__(self):
        self.isCancelled = False

    def cancel(self):
        self.isCancelled = True

    def call(self):
        for module in event_listeners.values():
            if self.__class__ in module:
                for priority in sorted(module[self.__class__].keys(), key=lambda x: x.value):
                    for listener in module[self.__class__][priority]:
                        LoggerManager.log_exception(True)(listener)(self)
                        if self.isCancelled:
                            return None


def event_listener(event_class: type, priority: Priority = Priority.NORMAL):
    if not isinstance(event_class, type) or not issubclass(event_class, Event):
        raise TypeError("event_listener() arg 1 must be a event class")
    if not isinstance(priority, Priority):
        raise TypeError("event_listener() arg 2 must be a priority")

    def wrapper(func):
        params_len = len(inspect.signature(func).parameters)
        if params_len != 1:
            raise TypeError(
                "the listener takes {} positional arguments but 1 and only 1 will be given".format(params_len))
        (event_listeners.setdefault(func.__module__, {})
         .setdefault(event_class, dict())
         .setdefault(priority, []).append(func))
        return func

    return wrapper


def unregister_listener(func):
    for module in event_listeners.values():
        for clazz in module.values():
            for listeners in clazz.values():
                if func in listeners:
                    listeners.remove(func)


def unregister_module(module):
    event_listeners.pop(module)
