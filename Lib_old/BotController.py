import Lib.core.Configs as Configs
import Lib.OnebotAPI as OnebotAPI
import Lib.QQRichText as QQRichText
import Lib.core.Logger as Logger
import Lib.QQDataCacher as QQDataCacher

api = OnebotAPI.OnebotAPI()
logger = Logger.logger


config = Configs.GlobalConfig()


def send_message(message: QQRichText.QQRichText | str, group_id: int = 0, user_id: int = 0):
    if group_id == 0 and user_id == 0:
        raise ValueError("group_id and user_id cannot be both 0")
    elif group_id != 0 and user_id != 0:
        raise ValueError("group_id and user_id cannot be both not 0")
    elif group_id != 0:
        api.send_group_msg(group_id, QQRichText.QQRichText(message).get_array())
        logger.info(f"发送消息 {message} 到群 {QQDataCacher.get_group_data(group_id).group_name}({group_id}) ")
    elif user_id != 0:
        api.send_private_msg(user_id, QQRichText.QQRichText(message).get_array())
        logger.info(f"发送消息 {message} 到 {QQDataCacher.get_user_data(user_id).nickname}({user_id}) ")


""" 还没写完，先注释掉
class BotINFO:
    def __init__(self, bot_id: int):
        self.bot_id = bot_id
        self.bot_name = ""
        self.bot_nickname = ""
        self.bot_sex = ""
        self.bot_age = ""
        self.bot_level = ""
        self.bot_role = ""
        self.bot_area = ""
        self.bot_join_time = ""
        self.bot_last_sent_time = ""
        self.bot_is_online = ""
"""


class Event:
    def __init__(self, event_json: dict):
        self.event_json: dict = event_json
        self.time: int = self["time"]
        self.self_id: int = self["self_id"]
        self.post_type: str = self["post_type"]

        if self.post_type == "message" or self.post_type == "message_sent":
            self.message_type: str = self["message_type"]
            self.user_id: int = int(self["user_id"])
            self.sub_type: str = self["sub_type"]

            self.message: QQRichText.QQRichText = QQRichText.QQRichText(self["message"])
            self.raw_message: str = str(self.message)
            self.message_id: int = self["message_id"]

            if self.message_type == "group":
                self.group_id: int = int(self["group_id"])
                self.sender: dict = self["sender"]

            elif self.message_type == "private":
                self.sender: dict = self["sender"]

        elif self.post_type == "notice":
            self.notice_type: str = self["notice_type"]

            if self.notice_type == "group_upload":
                self.group_id: int = int(self["group_id"])
                self.user_id: int = int(self["user_id"])
                self.file: dict = self["file"]

            elif self.notice_type == "group_decrease":
                self.group_id: int = int(self["group_id"])
                self.operator_id: int = self["operator_id"]
                self.user_id: int = int(self["user_id"])
                self.sub_type: str = self["sub_type"]

            elif self.notice_type == "group_increase":
                self.group_id: int = int(self["group_id"])
                self.user_id: int = int(self["user_id"])
                self.sub_type: str = self["sub_type"]
                self.operator_id: int = self["operator_id"]

            elif self.notice_type == "group_ban":
                self.group_id: int = int(self["group_id"])
                self.operator_id: int = self["operator_id"]
                self.user_id: int = int(self["user_id"])
                self.duration: int = self["duration"]
                self.sub_type: str = self["sub_type"]

            elif self.notice_type == "group_admin":
                self.group_id: int = int(self["group_id"])
                self.user_id: int = int(self["user_id"])
                self.sub_type: str = self["sub_type"]

            elif self.notice_type == "group_recall":
                self.group_id: int = int(self["group_id"])
                self.user_id: int = int(self["user_id"])
                self.message_id: int = self["message_id"]
                self.operator_id: int = self["operator_id"]

            elif self.notice_type == "friend_add":
                self.user_id: int = int(self["user_id"])

            elif self.notice_type == "friend_recall":
                self.message_id: int = self["message_id"]

            elif self.notice_type == "notify":
                self.sub_type: str = self["sub_type"]
                if self.sub_type == "poke":
                    self.group_id: int = int(self["group_id"])
                    self.user_id: int = int(self["user_id"])
                    self.target_id: int = self["target_id"]

                elif self.sub_type == "lucky_king":
                    self.group_id: int = int(self["group_id"])
                    self.user_id: int = int(self["user_id"])
                    self.target_id: int = self["target_id"]

                elif self.sub_type == "honor":
                    self.group_id: int = int(self["group_id"])
                    self.honor_type: str = self["honor_type"]
                    self.user_id: int = int(self["user_id"])

        elif self.post_type == "request":
            self.request_type: str = self["request_type"]

            if self.request_type == "friend":
                self.user_id: int = int(self["user_id"])
                self.comment: str = self["comment"]
                self.flag: str = self["flag"]

            elif self.request_type == "group":
                self.sub_type: str = self["sub_type"]
                self.group_id: int = int(self["group_id"])
                self.user_id: int = int(self["user_id"])
                self.comment: str = self["comment"]
                self.flag: str = self["flag"]

        elif self.post_type == "meta_event":
            self.meta_event_type = self["meta_event_type"]

            if self.meta_event_type == "lifecycle":
                self.sub_type: str = self["sub_type"]

            elif self.meta_event_type == "heartbeat":
                self.status: dict = self["status"]
                self.interval: int = self["interval"]

    def __getitem__(self, item):
        return self.event_json.get(item)

    def __contains__(self, other):
        return other in self.event_json

    def __repr__(self):
        return str(self.event_json)
