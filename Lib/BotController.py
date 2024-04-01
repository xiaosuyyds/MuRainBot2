import Lib.Configs as Configs
import Lib.OnebotAPI as OnebotAPI
import Lib.QQRichText as QQRichText

api = OnebotAPI.OnebotAPI()


def init():
    global api
    config = Configs.GlobalConfig()
    api.set_ip(config.api_host, config.api_port)


def send_message(message: QQRichText.QQRichText | str, group_id: int = 0, user_id: int = 0):
    if group_id == 0 and user_id == 0:
        raise ValueError("group_id and user_id cannot be both 0")
    elif group_id != 0 and user_id != 0:
        raise ValueError("group_id and user_id cannot be both not 0")
    elif group_id != 0:
        api.get("/send_msg", {"group_id": group_id, "message": message})
    elif user_id != 0:
        api.get("/send_private_msg", {"user_id": user_id, "message": message})


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


class Event:
    def __init__(self, event_json: dict):
        self.event_json = event_json
        self.time = self["time"]
        self.self_id = self["self_id"]
        self.post_type = self["post_type"]

        if self.post_type == "message" or self.post_type == "message_sent":
            self.message_type = self["message_type"]
            self.user_id = self["user_id"]
            self.sub_type = self["sub_type"]

            self.message = QQRichText.QQRichText(self["message"])
            self.message_id = self["message_id"]

            if self.message_type == "group":
                self.group_id = self["group_id"]
                self.sender = self["sender"]

            elif self.message_type == "private":
                self.sender = self["sender"]

        elif self.post_type == "notice":
            self.notice_type = self["notice_type"]

            if self.notice_type == "group_upload":
                self.group_id = self["group_id"]
                self.user_id = self["user_id"]
                self.file = self["file"]

            elif self.notice_type == "group_decrease":
                self.group_id = self["group_id"]
                self.operator_id = self["operator_id"]
                self.user_id = self["user_id"]
                self.sub_type = self["sub_type"]

            elif self.notice_type == "group_increase":
                self.group_id = self["group_id"]
                self.user_id = self["user_id"]
                self.sub_type = self["sub_type"]

            elif self.notice_type == "group_ban":
                self.group_id = self["group_id"]
                self.operator_id = self["operator_id"]
                self.user_id = self["user_id"]
                self.duration = self["duration"]
                self.sub_type = self["sub_type"]

            elif self.notice_type == "group_admin":
                self.group_id = self["group_id"]
                self.user_id = self["user_id"]

            elif self.notice_type == "group_recall":
                self.group_id = self["group_id"]
                self.user_id = self["user_id"]
                self.message_id = self["message_id"]

            elif self.notice_type == "friend_add":
                self.user_id = self["user_id"]

            elif self.notice_type == "friend_recall":
                self.message_id = self["message_id"]

            elif self.notice_type == "group_recall":
                self.group_id = self["group_id"]
                self.user_id = self["user_id"]
                self.message_id = self["message_id"]

            elif self.notice_type == "notify" and self["sub_type"] == "poke":
                self.user_id = self["user_id"]
                self.target_id = self["target_id"]
                self.notice_type = "poke"
                self.sub_type = self["sub_type"]
                self.group_id = self["group_id"]

            elif self.notice_type == "notify" and self["sub_type"] == "lucky_king":
                self.user_id = self["user_id"]
                self.group_id = self["group_id"]
                self.target_id = self["target_id"]
                self.notice_type = "lucky_king"
                self.sub_type = self["sub_type"]

            elif self.notice_type == "notify" and self["sub_type"] == "honor":
                self.user_id = self["user_id"]
                self.group_id = self["group_id"]
                self.honor_type = self["honor_type"]
                self.notice_type = "honor"
                self.sub_type = self["sub_type"]

        elif self.post_type == "request":
            self.request_type = self["request_type"]

            if self.request_type == "friend":
                self.user_id = self["user_id"]
                self.comment = self["comment"]
                self.flag = self["flag"]

            elif self.request_type == "group":
                self.user_id = self["user_id"]
                self.group_id = self["group_id"]
                self.comment = self["comment"]
                self.flag = self["flag"]

        elif self.post_type == "meta_event":
            self.meta_event_type = self["meta_event_type"]

            if self.meta_event_type == "lifecycle":
                self.sub_type = self["sub_type"]

            elif self.meta_event_type == "heartbeat":
                self.status = self["status"]
                self.interval = self["interval"]

    def __getitem__(self, item):
        return self.event_json.get(item)
