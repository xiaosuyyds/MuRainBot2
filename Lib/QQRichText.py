# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|
# Code with by Xiaosu & Evan. Copyright (c) 2024 GuppyTEAM. All rights reserved.
# 本代码由校溯 和 XuFuyu编写。版权所有 （c） 2024 Guppy团队。保留所有权利。
"""
QQRichText
QQ富文本处理
"""

import re


# CQ解码
def cq_decode(text) -> str:
    text = str(text)
    return text.replace("&amp;", "&").replace("&#91;", "["). \
        replace("&#93;", "]").replace("&#44;", ",")


# CQ编码
def cq_encode(text) -> str:
    text = str(text)
    return text.replace("&", "&amp;").replace("[", "&#91;"). \
        replace("]", "&#93;").replace(",", "&#44;")


class Text:
    def __init__(self, text: str) -> None:
        self.text = text
        self.raw_text = cq_decode(text)
        self.content = {"type": "text", "data": {"text": self.raw_text}}

    def set(self, text: str) -> None:
        self.text = text
        self.raw_text = cq_encode(text)

    def get(self) -> str:
        return self.text

    def get_raw_text(self) -> str:
        return self.raw_text

    def __str__(self):
        return self.raw_text

    def __repr__(self):
        return str(self.content)


class Face:
    def __init__(self, face_id: int) -> None:
        self.id = face_id
        self.content = {"type": "face", "data": {"id": self.id}}

    def set(self, face_id: int) -> None:
        self.id = face_id

    def get(self) -> int:
        return self.id

    def __str__(self):
        return "[CQ:face,id={}]".format(self.id)

    def __repr__(self):
        return str(self.content)


# class Record:
#     def __init__(self, face_id: int) -> None:
#         self.id = face_id
#         self.content = {"type": "record", "data": {"id": self.id}}
#
#     def set(self, face_id: int) -> None:
#         self.id = id
#
#     def get(self) -> int:
#         return self.id
#
#     def __str__(self):
#         return "[CQ:face,id={}]".format(self.id)
#
#     def __repr__(self):
#         return str(self.content)


class QQRichText:
    def __init__(self, rich_list: list = None, rich_text: str = ""):
        if rich_list is None:
            rich_list = []
        if rich_text != "":
            self.rich_text = rich_text
            pattern = r"\[CQ:(\w+)(?:,([^\]]+))?\]"
            text = ""
            cq = ""
            flag = False
            for i in rich_text:
                if i == "[":
                    # 文本消息
                    if text != "":
                        rich_list.append(
                            {
                                "type": "text",
                                "data": {
                                    "text": cq_decode(text)
                                }
                            }
                        )
                        text = ""
                    cq = "["
                    flag = True
                elif i == "]":
                    # CQ起始
                    cq += "]"
                    flag = False
                    rich = re.findall(pattern, cq)
                    rich_type = rich[0][0]
                    rich_data = rich[0][1]
                    rich_list.append(
                        {
                            "type": rich_type,
                            "data": dict(  # CQ码参数
                                cq_decode(x)
                                .split("=", 1) for x in rich_data.split(",")
                            ) if rich_data else {},
                        }
                    )
                elif flag:
                    cq += i
                else:
                    text += i
            if text != "":
                rich_list.append(
                    {
                        "type": "text",
                        "data": {
                            "text": cq_decode(text)
                        }
                    }
                )
        self.rich_list = rich_list

    def __str__(self):
        self.rich_text = ""
        for rich in self.rich_list:
            if rich["type"] == "text":
                self.rich_text += rich["data"]["text"]
            else:
                self.rich_text += "[CQ:{}".format(rich["type"])
                if rich["data"]:
                    for rich_type, rich_data in rich["data"].items():
                        self.rich_text += ",{}:{}".format(rich_type, rich_data)
                self.rich_text += "]"
        return self.rich_text

    def __repr__(self):
        return str(self.rich_list)

    def get(self):
        return self.rich_list
