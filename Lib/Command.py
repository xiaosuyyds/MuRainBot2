import Lib.OnebotAPI as OnebotAPI
import Lib.BotController as BotController
import Lib.QQRichText as QQRichText
import Lib.Logger as Logger

logger = Logger.logger


def start_listening_command():
    while True:
        input_command = input()
        if input_command[0] == "/":
            input_command = input_command[1:]

        logger.debug(f"Command: {input_command}")

        if input_command == "exit":
            exit()

        elif input_command.startswith("send_group_msg"):
            command = input_command.split(" ")
            try:
                group_id = int(command[1])
            except ValueError:
                logger.error("group_id 必须是一个数字")
                continue

            BotController.send_message(command[2], group_id=group_id)

        elif input_command.startswith("send_msg"):
            command = input_command.split(" ")
            try:
                user_id = int(command[1])
            except ValueError:
                logger.error("user_id 必须是一个数字")
                continue

            BotController.send_message(command[2], user_id=user_id)

        elif input_command == "help":
            print("""MuRainBot2命令帮助：
exit: 退出程序
send_msg <user_id> <message>: 发送消息到好友
send_group_msg <group_id> <message>: 发送消息到群
help: 查看帮助""")
        else:

            logger.error("未知的命令, 请发送help查看支持的命令")
