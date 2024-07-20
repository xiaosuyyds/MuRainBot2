import Lib.BotController as BotController
import Lib.QQRichText as QQRichText
import Lib.OnebotAPI as OnebotAPI
import Lib.MuRainLib as MuRainLib
import os
import Lib.Logger as Logger

logger = Logger.logger

commands = []


class Meta(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        if 'Command' in globals() and issubclass(cls, Command):
            commands.append(cls())  # 将子类添加到全局列表中


class Command(metaclass=Meta):
    def __init__(self):
        self.command_help = ""  # 命令帮助

    def check(self, input_command: str):
        # 判断输入的命令是否是这个命令
        pass

    def run(self, input_command: str):
        # 执行命令
        pass


class SendGroupMsgCommand(Command):
    def __init__(self):
        super().__init__()
        self.command_help = "send_group_msg <group_id> <message>: 发送消息到群"

    def check(self, input_command: str):
        return input_command.startswith("send_group_msg")

    def run(self, input_command: str):
        command = input_command.split(" ")
        try:
            group_id = int(command[1])
        except ValueError:
            logger.error("group_id 必须是一个数字")
            return

        BotController.send_message(QQRichText.QQRichText(" ".join(command[2:])), group_id=group_id)


class SendMsgCommand(Command):
    def __init__(self):
        super().__init__()
        self.command_help = "send_msg <user_id> <message>: 发送消息到好友"

    def check(self, input_command: str):
        return input_command.startswith("send_msg")

    def run(self, input_command: str):
        command = input_command.split(" ")
        try:
            user_id = int(command[1])
        except ValueError:
            logger.error("user_id 必须是一个数字")
            return

        BotController.send_message(QQRichText.QQRichText(" ".join(command[2:])), user_id=user_id)


class ExitCommand(Command):
    def __init__(self):
        super().__init__()
        self.command_help = "exit: 退出程序"

    def check(self, input_command: str):
        return input_command == "exit"

    def run(self, input_command: str):
        logger.info("MuRainBot即将关闭，正在删除缓存")
        MuRainLib.clean_cache()
        logger.warning("MuRainBot结束运行！")
        logger.info("再见！\n")
        os._exit(0)



class RunAPICommand(Command):
    def __init__(self):
        super().__init__()
        self.command_help = "run_api <api_name:api节点> <api_params: api参数dict格式(可选)>: 运行API"

    def check(self, input_command: str):
        return input_command.startswith("run_api")

    def run(self, input_command: str):
        command = input_command.split(" ")
        api_name = command[1]
        if len(command) > 2:
            api_params = eval(" ".join(command[2:]))
        else:
            api_params = {}
        print(OnebotAPI.OnebotAPI().get(api_name, api_params))


class HelpCommand(Command):
    def __init__(self):
        super().__init__()
        self.command_help = "help: 查看帮助"

    def check(self, input_command: str):
        return input_command == "help"

    def run(self, input_command: str):
        help_text = "MuRainBot2命令帮助：\n" + "\n".join([command.command_help for command in commands])
        print(help_text)


def check_command(input_command: str):
    filtered_commands = list(filter(lambda command: command.check(input_command), commands))
    return filtered_commands[0] if len(filtered_commands) > 0 else None


def start_listening_command():
    while True:
        input_command = input()
        if len(input_command) == 0:
            continue

        if input_command[0] == "/":
            input_command = input_command[1:]

        logger.debug(f"Command: {input_command}")

        try:
            command = check_command(input_command)
        except Exception as e:
            logger.error(f"检查命令时发生错误: {e}")
            return

        if command is not None:
            try:
                command.run(input_command)
            except Exception as e:
                logger.error(f"执行命令时发生错误: {e}")
        else:
            logger.error("未知的命令, 请发送help查看支持的命令")


if __name__ == "__main__":
    start_listening_command()
