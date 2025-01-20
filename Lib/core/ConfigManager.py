import dataclasses

import yaml
from ..constants import *
from ..utils import Logger

logger = Logger.logger


class ConfigManager:
    def __init__(self, config_path, default_config: str | dict = None):
        self.config_path = config_path
        self.default_config = default_config
        self.config = {}
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, encoding="utf-8") as f:
                    self.config = yaml.safe_load(f)
            except Exception as e:
                logger.error(f"配置文件加载失败，请检查配置文件内容是否正确。"
                             f"如果无法修复，请删除配置文件重新配置，以创建默认配置文件。"
                             f"错误信息：{repr(e)}")
        else:
            try:
                if isinstance(self.default_config, str):
                    with open(self.config_path, "w", encoding="utf-8") as f:
                        f.write(self.default_config)
                        logger.info("配置文件不存在，已创建默认配置文件")
                    self.load_config()
                elif isinstance(self.default_config, dict):
                    with open(self.config_path, "w", encoding="utf-8") as f:
                        yaml.safe_dump(self.default_config, f)
                        logger.info("配置文件不存在，已创建默认配置文件")
                    self.load_config()
                else:
                    logger.error("配置文件不存在，且未提供默认配置，无法创建默认配置文件")
                    self.config = {}
            except Exception as e:
                logger.error(f"配置文件创建失败，请检查配置文件路径是否正确。错误信息：{repr(e)}")
                self.config = {}
        self.init()

    def init(self):
        """
        用于初始化配置文件，可自行编写初始化逻辑，例如默认值等
        """
        pass

    def save_config(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.config, f)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.init()


class GlobalConfig(ConfigManager):
    _instance = None
    _init_flag = False

    @dataclasses.dataclass
    class Account:
        user_id: int
        nick_name: str
        bot_admin: list

    @dataclasses.dataclass
    class Api:
        host: str
        port: int

    @dataclasses.dataclass
    class Server:
        host: str
        port: int
        max_works: int

    @dataclasses.dataclass
    class ThreadPool:
        max_workers: int

    @dataclasses.dataclass
    class QQDataCache:
        enable: bool
        expire_time: int
        max_cache_size: int

    @dataclasses.dataclass
    class Debug:
        enable: bool

    @dataclasses.dataclass
    class AutoRestartOnebot:
        enable: bool

    DEFAULT_CONFIG = """# MuRainBot2配置文件
account:  # 账号相关
  user_id: 0  # QQ账号（留空则自动获取）
  nick_name: ""  # 昵称（留空则自动获取）
  bot_admin: []

api:  # Api设置
  host: '127.0.0.1'
  port: 5700

server:  # 监听服务器设置
  host: '127.0.0.1'
  port: 5701
  max_works: 4  # 最大工作线程数

thread_pool:  # 线程池相关
  max_workers: 10  # 线程池最大线程数

qq_data_cache:  # QQ数据缓存设置
  enable: true  # 是否启用缓存（非常不推荐关闭缓存，对于对于需要无缓存的场景，推荐在插件内自行调用api来获取而非关闭此配置项）
  expire_time: 300  # 缓存过期时间（秒）
  max_cache_size: 500  # 最大缓存数量（设置过大可能会导致报错）


debug:  # 调试模式，若启用框架的日志等级将被设置为debug，不建议在生产环境开启
  enable: false  # 是否启用调试模式

auto_restart_onebot:  # 在Onebot实现端状态异常时自动重启Onebot实现端（需开启心跳包）
  enable: true  # 是否启用自动重启

"""

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.account: GlobalConfig.Account = None
        self.api: GlobalConfig.Api = None
        self.server: GlobalConfig.Server = None
        self.thread_pool: GlobalConfig.ThreadPool = None
        self.qq_data_cache: GlobalConfig.QQDataCache = None
        self.debug: GlobalConfig.Debug = None
        self.auto_restart_onebot: GlobalConfig.AutoRestartOnebot = None
        if not self._init_flag:
            self._init_flag = True
            super().__init__(CONFIG_PATH, self.DEFAULT_CONFIG)
        else:
            self.init()

    def init(self):
        super().init()
        self.account = self.Account(
            user_id=self.get("account", {}).get("user_id", 0),
            nick_name=self.get("account", {}).get("nick_name", ""),
            bot_admin=self.get("account", {}).get("bot_admin", [])
        )
        self.api = self.Api(
            host=self.get("api", {}).get("host", ""),
            port=self.get("api", {}).get("port", 5700)
        )
        self.server = self.Server(
            host=self.get("server", {}).get("host", ""),
            port=self.get("server", {}).get("port", 5701),
            max_works=self.get("server", {}).get("max_works", 4)
        )
        self.thread_pool = self.ThreadPool(
            max_workers=self.get("thread_pool", {}).get("max_workers", 10)
        )
        self.qq_data_cache = self.QQDataCache(
            enable=self.get("qq_data_cache", {}).get("enable", True),
            expire_time=self.get("qq_data_cache", {}).get("expire_time", 300),
            max_cache_size=self.get("qq_data_cache", {}).get("max_cache_size", 500)
        )
        self.debug = self.Debug(
            enable=self.get("debug", {}).get("enable", False)
        )
        self.auto_restart_onebot = self.AutoRestartOnebot(
            enable=self.get("auto_restart_onebot", {}).get("enable", True)
        )


if __name__ == "__main__":
    test_config = GlobalConfig()
    print(test_config.api)
    test_config.set("api", {"host": "127.0.0.1", "port": 5700})
    print(test_config.api)
