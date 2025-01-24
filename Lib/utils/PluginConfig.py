import traceback

from Lib.core import ConfigManager
from Lib.constants import *


class PluginConfig(ConfigManager.ConfigManager):
    def __init__(
            self,
            plugin_name: str = os.path.splitext(os.path.split(traceback.extract_stack()[-2].filename)[-1])[0],
            default_config: str | dict = None
    ):
        super().__init__(os.path.join(PLUGIN_CONFIGS_PATH, f"{plugin_name}.yml"), default_config)
        self.plugin_name = plugin_name
