import yaml
import os
import traceback

global_config = None


class Config:
    def __init__(self, path):
        self.raw_config = None
        self.path = path
        self.encoding = "utf-8"

    def reload(self):
        with open(self.path, encoding=self.encoding) as file:
            self.raw_config = yaml.load(file.read(), yaml.FullLoader)
        return self

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


class GlobalConfig(Config):
    def __init__(self):
        super().__init__("config.yml")
        self.reload()
        self.user_id = self.raw_config["account"]["user_id"]
        self.nick_name = self.raw_config["account"]["nick_name"]
        self.bot_admin = self.raw_config["account"]["bot_admin"]
        self.server_host = self.raw_config["server"]["host"]
        self.server_port = self.raw_config["server"]["port"]
        self.api_host = self.raw_config["api"]["host"]
        self.api_port = self.raw_config["api"]["port"]
        self.max_workers = self.raw_config["thread_pool"]["max_workers"]
