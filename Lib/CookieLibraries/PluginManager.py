# coding: utf-8
import importlib

# MIT License
#
# Copyright (c) 2024 BigCookie233
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import Lib.CookieLibraries.EventManager as EventManager


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
