# coding: utf-8

# Created by BigCookie233

import yaml


class Config:
    def __init__(self, path):
        self.raw_config = None
        self.path = path
        self.reload()

    def reload(self):
        with open(self.path, encoding="utf-8") as file:
            self.raw_config = yaml.load(file.read(), yaml.FullLoader)
