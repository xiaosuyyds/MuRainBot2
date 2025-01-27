"""
插件配置管理
"""

import traceback

from Lib.core import ConfigManager, PluginManager
from Lib.constants import *


class PluginConfig(ConfigManager.ConfigManager):
    """
    插件配置管理
    """
    def __init__(
            self,
            plugin_name: str = None,
            default_config: str | dict = None
    ):
        if plugin_name is None:
            plugin_path = traceback.extract_stack()[-2].filename
            for plugin in PluginManager.plugins:
                if os.path.samefile(plugin_path, plugin["file_path"]):
                    plugin_name = plugin["name"]
                    break
        super().__init__(os.path.join(PLUGIN_CONFIGS_PATH, f"{plugin_name}.yml"), default_config)
        self.plugin_name = plugin_name
