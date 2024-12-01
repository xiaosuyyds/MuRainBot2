import Lib.OnebotAPI as OnebotAPI
import Lib.QQRichText as QQRichText

api = OnebotAPI.OnebotAPI()


class Forward:
    def __init__(self):
        self.messages: list[QQRichText.Node] = []

    def add(self, message: QQRichText.QQRichText, user_id: int, nickname: str):
        self.messages.append(QQRichText.Node(nickname, user_id, message))

    def add_message_id(self, message_id: int):
        message_data = api.get_msg(message_id)
        message = QQRichText.QQRichText(message_data.get("message"))
        user_id = message_data.get("sender").get("user_id")
        nickname = message_data.get("sender").get("nickname")
        self.messages.append(QQRichText.Node(nickname, user_id, message))

    def build(self):
        # 警告：此处调用的API并非属于Onebot11标准api，需要onebot实现端支持此api
        data = {"messages": [{
            "type": "node",
            "data": {
                "nickname": m.name,
                "user_id": str(m.user_id),
                "content": m.message
            }
        } for m in self.messages]}
        res = api.get("send_forward_msg", data)
        return res
