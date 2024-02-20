#   __  __       ____       _         ____        _   
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_ 
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __|
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ 
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|

# Code with by Xiaosu. Copyright (c) 2023 Guppy team. All rights reserved.
# 本代码由由校溯写。版权所有 （c） 2023-2024 Guppy团队。保留所有权利。

from Lib import MuRainLib
from Lib import OnebotAPI
from Lib import QQRichText
import os
import logging

api = OnebotAPI.OnebotAPI()

config = {}


class PluginInfo:
    def __init__(self, config_):
        """
        :param config_:框架配置文件
        """
        global config
        config = config_
        self.NAME = "插件名称"  # 插件名称
        self.AUTHOR = "作者"  # 插件作者
        self.VERSION = "版本"  # 插件版本
        self.DESCRIPTION = "描述"  # 插件描述
        self.HELP_MSG = "帮助"  # 插件帮助

        api.set_ip(config["api"]["host"], config["api"]["port"])


# 发送群聊消息
def group_msg_send(group_id, message: str | QQRichText.QQRichText):
    gname = api.get("/get_group_info", {"group_id": group_id})["group_name"]
    logging.info("发送群 {}({}) 的消息: {}".format(gname, group_id, str(message)))
    api.get("/send_group_msg", {"group_id": group_id, "message": message})


# 主函数
def main(report, work_path):
    bot_name = config["account"]["name"]
    bot_uid = config["account"]["uin"]
    bot_admin = config["bot"]["admin"]

    # report:go-cqhttp上报的消息
    # work_path:data目录的路径
