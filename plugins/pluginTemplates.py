# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

from Lib import *

api = OnebotAPI.OnebotAPI()


# TODO: 插件信息后续从类改为函数，把初始化的也放进来。
class PluginInfo:
    def __init__(self):
        self.NAME = "HelloWorld"  # 插件名称
        self.AUTHOR = "You"  # 插件作者
        self.VERSION = "1.0.0"  # 插件版本
        self.DESCRIPTION = "一个发送HelloWorld的插件"  # 插件描述
        self.HELP_MSG = ""  # 插件帮助


# 写法1: 注册关键词
def say_hello(event_class, event_data: BotController.Event):
    if event_data.message_type == "private":  # 判断是群聊事件还是私聊事件
        BotController.send_message("Hello World!", user_id=event_data.user_id)
    else:
        BotController.send_message(QQRichText.QQRichText(QQRichText.At(event_data.user_id), "Hello World!"),
                                   group_id=event_data.group_id)


EventManager.register_keyword("hello", say_hello)


# 写法2: 主函数
def main(report, work_path):
    """
    :param report: 实现端上报的消息
    :param work_path: main.py所在的路径
    :return:
    """
    data = BotController.Event(report)
    if data.post_type == "message":
        message = data.message
        if message == "hello":
            if data.message_type == "private":
                BotController.send_message("Hello World!", user_id=data.user_id)
            else:
                BotController.send_message(QQRichText.QQRichText(QQRichText.At(data.user_id), "Hello World!"),
                                           group_id=data.group_id)


# 写法3: 注册事件
@EventManager.register_event("message")
def on_message(event_class, event_data: BotController.Event):
    if event_data.message == "hello":  # 判断是群聊事件还是私聊事件
        if event_data.message_type == "private":
            BotController.send_message("Hello World!", user_id=event_data.user_id)
        else:
            BotController.send_message(QQRichText.QQRichText(QQRichText.At(event_data.user_id), "Hello World!"),
                                       group_id=event_data.group_id)


# 自定义控制台命令
class SayHelloCommand(Command.Command):
    def __init__(self):
        super().__init__()
        self.command_help = "say_hello <group_id: 要发送的群号> <user_id: 要私聊发送的用户uid>"
        self.command_name = "say_hello"
        self.need_args = {
            "group_id": {
                "type": int,
                "help": "要发送的群号",
                "default": 0,
                "must": False
            },
            "user_id": {
                "type": int,
                "help": "要私聊发送的用户uid",
                "default": 0,
                "must": False
            }
        }

    def run(self, input_command: Command.CommandParsing, kwargs):
        group_id = kwargs.get("group_id")
        user_id = kwargs.get("user_id")
        if group_id == 0 and user_id == 0:
            raise "必须要指定发送的群或者人"
        elif group_id == 0:
            BotController.send_message("hello", user_id=user_id)
        elif user_id == 0:
            BotController.send_message("hello", group_id=group_id)
        else:
            raise "不一起都设置群号和uid"
