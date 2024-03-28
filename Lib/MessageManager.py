# coding: utf-8

# Created by BigCookie233

import Lib.BotController as BotController


class Message:
    def __init__(self, raw_message):
        self.raw_message = raw_message

    def send_to_group(self, group_id):
        BotController.send_group_message(group_id, self.raw_message)


class ReceivedMessage(Message):
    def __init__(self, raw_message, message_id, sender):
        super().__init__(raw_message)
        self.message_id = message_id
        self.sender = sender


class ReceivedGroupMessage(ReceivedMessage):
    def __init__(self, raw_message, message_id, sender, group_id):
        super().__init__(raw_message, message_id, sender)
        self.group_id = group_id
