# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

from Lib import *
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
    """
    :param report: go-cqhttp上报的消息
    :param work_path: main.py所在的路径
    :return:
    """
    bot_name = config["account"]["nick_name"]
    bot_uid = config["account"]["user_id"]
    bot_admin = config["account"]["bot_admin"]
