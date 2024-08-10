#   __  __       ____       _         ____        _
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __|
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|
# Code with by Xiaosu. Copyright (c) 2023 Guppy team. All rights reserved.
# 本代码由由校溯写。版权所有 （c） 2023 Guppy团队。保留所有权利。
import Lib.PluginManager
from Lib import *

api = OnebotAPI.OnebotAPI()


class PluginInfo(PluginManager.PluginInfo):
    def __init__(self):
        super().__init__()
        self.NAME = "Helper"  # 插件名称
        self.AUTHOR = "校溯"  # 插件作者
        self.VERSION = "1.0"  # 插件版本
        self.DESCRIPTION = "帮助插件"  # 插件描述
        self.HELP_MSG = "发送/help，或者/帮助即可查看帮助"  # 插件帮助


def get_help_text():
    plugins = Lib.PluginManager.plugins
    text = "MuRainBot2帮助"
    for plugin in plugins:
        try:
            plugin_info = plugin["plugin"].PluginInfo()
            if plugin_info.HELP_MSG and plugin_info.IS_HIDDEN is False:
                text += "\n{} - {}".format(plugin_info.NAME, plugin_info.HELP_MSG)
        except:
            pass
    return text


def help(event_type, event_data):
    BotController.send_message(
        QQRichText.QQRichText(
            QQRichText.Reply(event_data["message_id"]),
            get_help_text()
        ), group_id=event_data["group_id"]
    )


EventManager.register_keyword("/help", help, model="EQUAL")
EventManager.register_keyword("/帮助", help, model="EQUAL")
