# coding: utf-8

# Created by BigCookie233

import Lib.EventManager as EventManager
import Lib.PluginManager as PluginManager


class ReceiveMessageEvent(EventManager.Event):
    def __init__(self, message):
        super().__init__()
        self.message = message


class ReceiveGroupMessageEvent(ReceiveMessageEvent):
    def __init__(self, message):
        super().__init__(message)


def on_enable(func):
    return EventManager.event_listener(PluginManager.PluginEnableEvent)(func)


def on_disable(func):
    return EventManager.event_listener(PluginManager.PluginDisableEvent)(func)


def on_message(func):
    return EventManager.event_listener(ReceiveMessageEvent)(func)


def on_group_message(func):
    return EventManager.event_listener(ReceiveGroupMessageEvent)(func)
