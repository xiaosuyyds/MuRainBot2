# coding: utf-8

# Created by BigCookie233

import importlib

import CookieLibraries.EventManager as EventManager


class PluginEnableEvent(EventManager.Event):
    def __init__(self, plugin):
        self.plugin = plugin

    def call(self):
        if self.__class__ in EventManager.event_listeners:
            for listener in EventManager.event_listeners[self.__class__]:
                if listener.__module__ == self.plugin.__name__:
                    listener(self)


class Plugin:
    def __init__(self, name, package="plugins"):
        self.version = None
        self.instance = None
        self.name = name
        self.package = package

    def load(self):
        try:
            self.instance = importlib.import_module(name=self.name, package=self.package)
            self.version = self.instance.PLUGIN_VERSION
            PluginEnableEvent(self.instance).call()
            # TODO: 禁用插件事件
        except Exception as e:
            self.instance = None
            self.version = None
            # TODO: 使用日志库打印异常信息
            print(e)
