# coding: utf-8

# Created by BigCookie233

import os
import traceback

import yaml

import Lib.Logger as LoggerManager
import Lib.FileCacher as FileCacher


class Config:
    def __init__(self, path):
        self.raw_config = None
        self.path = path
        self.encoding = "utf-8"

    @LoggerManager.log_exception()
    def reload(self):
        self.raw_config = yaml.load(FileCacher.read_file(self.path, self.encoding), yaml.FullLoader)
        return self

    @LoggerManager.log_exception()
    def save_default(self, default_config: str):
        if isinstance(default_config, str):
            FileCacher.write_non_existent_file(self.path, default_config, self.encoding)
        else:
            raise TypeError("default config must be a string")
        return self


class PluginConfig(Config):
    def __init__(self):
        super().__init__(os.path.join("configs", traceback.extract_stack()[-2].filename.rsplit(".", 1)[0] + ".yml"))
