import Lib.BotController as BotController
import Lib.EventManager
import Lib.QQRichText as QQRichText
import Lib.OnebotAPI as OnebotAPI
import Lib.MuRainLib as MuRainLib
import os
import Lib.Logger as Logger

logger = Logger.logger

commands = []


class CommandParsing:
    def __init__(self, input_command: str):
        self.input_command = input_command
        self.command = None
        self.command_args = None
        self.command_list = self.parse()
        self.command = self.command_list[0]
        self.command_args = [_ for _ in self.command_list[1:] if isinstance(_, str)] \
            if len([_ for _ in self.command_list if isinstance(_, str)]) > 1 else []
        self.command_kwargs = {
            k: v for d in [_ for _ in self.command_list if isinstance(_, dict)] for k, v in d.items()
        }

    def parse(self):
        flag = True
        is_in_quote = False
        now_quote_type = None
        is_escape = False
        counter = 0
        command_list = []
        now_command = ""
        for s in self.input_command:
            if s == "\\" and not is_escape:
                is_escape = True
            elif s == "\\" and is_escape:
                now_command += s
                is_escape = False
            elif s == '"' and now_quote_type != "'" and not is_escape:
                is_in_quote = not is_in_quote
                now_quote_type = '"' if is_in_quote else None
            elif s == '"' and now_quote_type != "'" and is_escape:
                now_command += s
                is_escape = False
            elif s == "'" and now_quote_type != '"' and not is_escape:
                is_in_quote = not is_in_quote
                now_quote_type = "'" if is_in_quote else None
            elif s == "'" and now_quote_type != '"' and is_escape:
                now_command += s
                is_escape = False
            elif s == ' ' and not is_in_quote:
                if flag:
                    if "=" in now_command:
                        now_command = now_command.split("=")
                        if len(now_command) == 2:
                            command_list.append({now_command[0]: now_command[1]})
                        else:
                            raise Exception("命令格式错误")
                    else:
                        command_list.append(now_command)
                    now_command = ""
                else:
                    flag = True
                counter += 1
            else:
                now_command += s

        if flag:
            if "=" in now_command:
                now_command = now_command.split("=")
                if len(now_command) == 2:
                    command_list.append({now_command[0]: now_command[1]})
                else:
                    raise Exception("命令格式错误")
            else:
                command_list.append(now_command)
        return command_list


class Meta(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        if 'Command' in globals() and issubclass(cls, Command):
            commands.append(cls())  # 将子类添加到全局列表中


class Command(metaclass=Meta):
    def __init__(self):
        self.command_help = ""  # 命令帮助
        self.need_args = None  # 需要的参数(None即不需要)
        self.command_name = ""  # 命令名
        """
        need_args = {
            "arg1": {  # 参数名
                "type": int,  # 类型
                "help": "参数1的帮助信息",  # 参数帮助信息
                "default": 0  # 默认值
                "must": True  # 是否必要   
            }
        """

    def run(self, input_command: CommandParsing, kwargs):
        # 执行命令
        pass


class SendGroupMsgCommand(Command):
    def __init__(self):
        super().__init__()
        self.command_help = "send_group_msg <group_id> <message>: 发送消息到群"
        self.command_name = "send_group_msg"
        self.need_args = {
            "group_id": {
                "type": int,
                "help": "要发送给的QQ群ID",
                "default": 0,
                "must": True
            },
            "message": {
                "type": str,
                "help": "发送的消息内容",
                "default": "",
                "must": True
            }
        }

    def run(self, input_command: CommandParsing, kwargs):
        BotController.send_message(QQRichText.QQRichText(kwargs.get("message")), group_id=kwargs.get("group_id"))


class SendMsgCommand(Command):
    def __init__(self):
        super().__init__()
        self.command_help = "send_msg <user_id> <message>: 发送消息到好友"
        self.command_name = "send_msg"
        self.need_args = {
            "user_id": {
                "type": int,
                "help": "要发送给的QQ用户ID",
                "default": 0,
                "must": True
            },
            "message": {
                "type": str,
                "help": "发送的消息内容",
                "default": "",
                "must": True
            }
        }

    def run(self, input_command: CommandParsing, kwargs):
        BotController.send_message(QQRichText.QQRichText(kwargs.get("message")), user_id=kwargs.get("user_id"))


class ExitCommand(Command):
    def __init__(self):
        super().__init__()
        self.command_help = "exit: 退出程序"
        self.command_name = "exit"

    def run(self, input_command: CommandParsing, **kwargs):
        logger.info("MuRainBot即将关闭，正在删除缓存")
        MuRainLib.clean_cache()
        logger.warning("MuRainBot结束运行！")
        logger.info("再见！\n")
        os._exit(0)


class RunAPICommand(Command):
    def __init__(self):
        super().__init__()
        self.command_help = "run_api <api_name:api节点> <api_params: api参数dict格式(可选)>: 运行API"
        self.command_name = "run_api"
        self.need_args = {
            "api_name": {
                "type": str,
                "help": "要运行的API节点",
                "default": "",
                "must": True
            },
            "api_params": {
                "type": dict,
                "help": "API参数",
                "default": {},
                "must": False
            }
        }
        self.api = OnebotAPI.OnebotAPI(original=True)

    def run(self, input_command: CommandParsing, kwargs):
        api_name = kwargs.get("api_name")
        api_params = kwargs.get("api_params")
        logger.debug(f"API: {api_name}, 参数: {api_params}")
        print(self.api.get(api_name, api_params)[1].json())


class HelpCommand(Command):
    def __init__(self):
        super().__init__()
        self.command_help = "help: 查看帮助"
        self.command_name = "help"

    def run(self, input_command: CommandParsing, kwargs):
        help_text = "MuRainBot2命令帮助：\n" + "\n".join([command.command_help for command in commands])
        print(help_text)


def run_command(input_command):
    try:
        run_command = None
        for command in commands:
            if input_command.command == command.command_name:
                run_command: Command = command
                break
    except Exception as e:
        logger.error(f"检查命令时发生错误: {e}")
        return
    if run_command is not None:
        try:
            kwargs = {}
            if run_command.need_args is not None and len(run_command.need_args) > 0:
                n = len(input_command.command_args)
                counter = len(
                    [arg_name for arg_name, arg_info in run_command.need_args.items() if arg_info["must"]])
                for arg_name, arg_info in run_command.need_args.items():
                    if n == 0:
                        break
                    if arg_info["must"]:
                        kwargs[arg_name] = input_command.command_args.pop(0)
                        if arg_info["type"] == int:
                            kwargs[arg_name] = int(kwargs[arg_name])
                        elif arg_info["type"] == float:
                            kwargs[arg_name] = float(kwargs[arg_name])
                        elif arg_info["type"] == bool:
                            kwargs[arg_name] = bool(kwargs[arg_name])
                        elif arg_info["type"] == dict or arg_info["type"] == list or arg_info["type"] == tuple:
                            kwargs[arg_name] = eval(kwargs[arg_name])
                        n -= 1
                        counter -= 1
                    else:
                        kwargs[arg_name] = arg_info["default"]

                for arg_name, arg_info in input_command.command_kwargs.items():
                    if arg_name in [_arg_name for _arg_name, _arg_info in run_command.need_args.items()]:
                        if arg_name not in kwargs:
                            counter -= 1
                        kwargs[arg_name] = arg_info
                        arg_type = run_command.need_args[arg_name]["type"]
                        if arg_type == int:
                            kwargs[arg_name] = int(kwargs[arg_name])
                        elif arg_type == float:
                            kwargs[arg_name] = float(kwargs[arg_name])
                        elif arg_type == bool:
                            kwargs[arg_name] = bool(kwargs[arg_name])
                        elif arg_type == dict or arg_info["type"] == list or arg_info["type"] == tuple:
                            kwargs[arg_name] = eval(kwargs[arg_name])

                if counter > 0:
                    raise Exception("缺少参数")

            run_command.run(input_command, kwargs)
        except Exception as e:
            logger.error(f"执行命令时发生错误: {e}")
    else:
        logger.error("未知的命令, 请发送help查看支持的命令")


def start_listening_command():
    while True:
        input_command = input()

        if len(input_command) == 0:
            continue

        if input_command[0] == "/":
            input_command = input_command[1:]
        input_command = CommandParsing(input_command)
        run_command(input_command)
        logger.debug(f"Command: {input_command.command_list}")


if __name__ == "__main__":
    start_listening_command()