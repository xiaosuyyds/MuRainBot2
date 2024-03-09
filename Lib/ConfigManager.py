# coding: utf-8

# MIT License
# Copyright (c) 2024 BigCookie233

import yaml


class Config:
    def __init__(self, path):
        self.raw_config = None
        self.path = path
        self.reload()

    def reload(self):
        with open(self.path, encoding="utf-8") as file:
            self.raw_config = yaml.load(file.read(), yaml.FullLoader)
