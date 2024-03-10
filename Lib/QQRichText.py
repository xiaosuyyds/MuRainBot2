# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

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


# 文本
class Text:
    def __init__(self, text: str) -> None:
        self.text = cq_encode(text)
        self.raw_text = text
        self.content = {"type": "text", "data": {"text": self.text}}

    def set(self, text: str) -> None:
        self.text = cq_encode(text)
        self.raw_text = text
        self.content = {"type": "text", "data": {"text": self.text}}

    @property
    def get(self) -> dict:
        return self.content

    def get_raw_text(self) -> str:
        return self.raw_text

    def __str__(self) -> str:
        return self.raw_text

    def __repr__(self) -> str:
        return str(self.content)


# 表情
class Face:
    def __init__(self, face_id: int) -> None:
        self.id = face_id
        self.content = {"type": "face", "data": {"id": self.id}}

    def set(self, face_id: int) -> None:
        self.id = face_id
        self.content = {"type": "face", "data": {"id": self.id}}

    @property
    def get(self) -> dict:
        return self.content

    def __str__(self) -> str:
        return "[CQ:face,id={}]".format(self.id)

    def __repr__(self) -> str:
        return str(self.content)


# 语音
class Record:
    def __init__(self, file: str, magic: bool | int = 0, cache: bool | int = 1, proxy: bool | int = 1,
                 timeout: int = -1) -> None:
        self.file = file
        self.magic = bool(magic)
        self.cache = bool(cache)
        self.proxy = bool(proxy)
        self.timeout = timeout
        if timeout != -1:
            self.content = {
                "type": "record", "data":
                    {
                        "file": self.file,
                        "magic": int(self.magic),
                        "cache": int(self.cache),
                        "proxy": int(self.proxy),
                        "timeout": self.timeout
                    }
            }
        else:
            self.content = {
                "type": "record", "data":
                    {
                        "file": self.file,
                        "magic": int(self.magic),
                        "cache": int(self.cache),
                        "proxy": int(self.proxy)
                    }
            }

    def set(self, file: str) -> None:
        self.file = file
        self.content["data"]["file"] = self.file

    @property
    def get(self) -> dict:
        return self.content

    def __str__(self):
        cq = "[CQ:record,file={}".format(self.file)
        if self.magic:
            cq += ",magic=1"
        if not self.cache:
            cq += ",cache=0"
        if self.timeout != -1:
            cq += ",timeout={}"
        return cq + "]"

    def __repr__(self):
        return str(self.content)


class At:
    def __init__(self, qq: int | str, name: str = "") -> None:
        if isinstance(qq, str) and qq != "all":
            raise ValueError("QQ号只能为数字或all")
        self.qq = qq
        self.name = name
        self.content = {"type": "at", "data": {"qq": self.qq, "name": name}}

    def set(self, qq: int) -> None:
        self.qq = qq
        self.content = {"type": "at", "data": {"qq": self.qq, "name": self.name}}

    @property
    def get(self) -> dict:
        return self.content

    def __str__(self) -> str:
        return "[CQ:at,qq={},name={}]".format(self.qq, self.name)

    def __repr__(self) -> str:
        return str(self.content)


class Image:
    def __init__(self, file: str, image_type: str = "", sub_type: int = 0,
                 cache: bool | int = True, id_: int = 40000, c: int = 1) -> None:
        self.file = file
        self.type = image_type
        self.subType = sub_type
        self.cache = bool(cache)
        self.id = id_
        self.c = c
        if not 0 >= sub_type >= 13:
            raise ValueError("未知的subType")
        if not 40000 >= id_ >= 40005:
            raise ValueError("未知的id")
        if not 1 >= c >= 3:
            raise ValueError("线程数过多/过少")
        if self.type != "" and self.type != "flash" and self.type != "show":
            raise ValueError("未知的图片类型")

        self.content = {"type": "image", "data": {"file": file}}
        if self.type != "":
            self.content["data"]["type"] = image_type

        if self.subType != 0:
            self.content["data"]["subType"] = sub_type

        if not self.cache:
            self.content["data"]["cache"] = 0

        if self.id != 40000:
            self.content["data"]["id"] = id_

        if self.c != 1:
            self.content["data"]["c"] = c

    def set(self, file: str) -> None:
        self.file = file
        self.content["data"]["file"] = file

    @property
    def get(self) -> dict:
        return self.content

    def __str__(self) -> str:
        cq = "[CQ:image,file={}".format(self.file)
        if self.type != "":
            cq += ",type={}"

        if self.subType != 0:
            cq += ",subType={}"

        if not self.cache:
            cq += ",cache=0"

        if self.id != 40000:
            cq += ",id={}"

        if self.c != 1:
            cq += ",c={}"

        return cq + "]"

    def __repr__(self):
        return str(self.content)


class Reply:
    def __init__(self, reply_id: int, text: str = "", qq: int = -1, time: int = -1, seq: int = -1) -> None:
        self.id = reply_id
        self.content = {"type": "reply", "data": {"id": self.id}}
        if text != "":
            self.content["text"] = text

        if qq != -1:
            self.content["qq"] = qq

        if time != -1:
            self.content["time"] = time

        if seq != -1:
            self.content["seq"] = seq

    def set(self, reply_id: int) -> None:
        self.id = reply_id
        self.content = {"type": "reply", "data": {"id": self.id}}

    @property
    def get(self) -> dict:
        return self.content

    def __str__(self) -> str:
        cq = "[CQ:reply,id={}".format(self.id)

        if "text" in self.content["data"]:
            cq += ",text={}"

        if "qq" in self.content["data"]:
            cq += ",qq={}"

        if "time" in self.content["data"]:
            cq += ",time={}"

        if "seq" in self.content["data"]:
            cq += ",seq={}"
        return cq + "]"

    def __repr__(self) -> str:
        return str(self.content)


class QQRichText:
    def __init__(self, rich_list: list | tuple = None, rich_text: str = ""):
        if rich_list is None:
            rich_list = []
        # 富文本解析
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
                    # CQ起始
                    cq = "["
                    flag = True
                elif i == "]":
                    # CQ结束
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

        self.rich_list = []
        for rich in rich_list:
            if isinstance(rich, dict):
                self.rich_list.append(rich)
            elif isinstance(rich, str):
                self.rich_list.append(Text(rich).get)
            else:
                try:
                    self.rich_list.append(rich.get)
                except TypeError:
                    self.rich_list.append(rich)

    def __str__(self):
        self.rich_text = ""
        for rich in self.rich_list:
            if isinstance(rich, dict):
                if rich["type"] == "text":
                    self.rich_text += rich["data"]["text"]
                else:
                    self.rich_text += "[CQ:{}".format(rich["type"])
                    if rich["data"]:
                        for rich_type, rich_data in rich["data"].items():
                            rich_type = cq_encode(cq_decode(rich_type))
                            rich_data = cq_encode(cq_decode(rich_data))
                            self.rich_text += ",{}={}".format(rich_type, cq_encode(rich_data))
                    self.rich_text += "]"
            elif isinstance(rich, str):
                self.rich_text += rich
            else:
                try:
                    self.rich_text += str(rich)
                except ValueError:
                    raise ValueError("QQRichText: rich_list contains a non-string or non-dict element")

        return self.rich_text

    def __repr__(self):
        return str(self.rich_list)

    def get(self):
        return self.rich_list

    def add(self, other):
        if isinstance(other, QQRichText):
            return QQRichText(self.rich_list + other.get())
        elif isinstance(other, dict):
            return QQRichText(self.rich_list + [other])
        elif isinstance(other, str):
            return QQRichText(self.rich_list + [{"type": "text", "data": {"text": other}}])
        else:
            try:
                return QQRichText(self.rich_list + [other.get])
            except ValueError:
                raise ValueError("QQRichText: rich_list contains a non-string or non-dict element")

    def __add__(self, other):
        return self.add(other)

    def __eq__(self, other):
        if isinstance(other, QQRichText):
            return self.rich_list == other.rich_list
        else:
            try:
                return str(self) == str(other)
            except ValueError:
                return False

    def __contains__(self, other):
        if isinstance(other, QQRichText):
            return all(item in self.rich_list for item in other.rich_list)
        else:
            try:
                return str(other) in str(self)
            except ValueError:
                return False


# 单元测试
if __name__ == "__main__":
    b = Face(1)

    c = QQRichText([
        Text("Hi"),
        Face(1),
        Record("https://gchat.qpic.cn/gchatpic_new/100000/100000/100000/0?term=2", False),
    ])

    print(b in c)
