#   __  __       ____       _         ____        _
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __|
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|

"""
Lagrange实现端扩展插件
"""

from Lib import *
from Lib.core import PluginManager

logger = Logger.get_logger()

plugin_info = PluginManager.PluginInfo(
    NAME="LagrangeExtension",
    AUTHOR="Xiaosu",
    VERSION="1.0.0",
    DESCRIPTION="用于支持一些Lagrange扩展的消息段和操作",
    HELP_MSG="",
    IS_HIDDEN=True
)


from plugins.LagrangeExtension import Actions, Segments
