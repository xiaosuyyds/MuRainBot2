# coding: utf-8

# Created by BigCookie233

import os
import traceback

import yaml

import Lib.Logger as LoggerManager


class Config:
    def __init__(self, path):
        self.raw_config = None
        self.path = path
        self.encoding = "utf-8"

    @LoggerManager.log_exception()
    def reload(self):
        with open(self.path, encoding=self.encoding) as file:
            self.raw_config = yaml.load(file.read(), yaml.FullLoader)
        return self

    @LoggerManager.log_exception()
    def save_default(self, default_config: str):
        if isinstance(default_config, str):
            if not os.path.exists(self.path):
                with open(self.path, "w", encoding=self.encoding) as file:
                    file.write(default_config)
        else:
            raise TypeError("default config must be a string")
        return self


class PluginConfig(Config):
    def __init__(self):
        super().__init__(os.path.join("configs", traceback.extract_stack()[-2].filename.rsplit(".", 1)[0] + ".yml"))
