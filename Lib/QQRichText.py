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
def cq_decode(text, in_cq: bool = False) -> str:
    text = str(text)
    if in_cq:
        return text.replace("&amp;", "&").replace("&#91;", "["). \
            replace("&#93;", "]").replace("&#44;", ",")
    else:
        return text.replace("&amp;", "&").replace("&#91;", "["). \
            replace("&#93;", "]")


# CQ编码
def cq_encode(text, in_cq: bool = False) -> str:
    text = str(text)
    if in_cq:
        return text.replace("&", "&amp;").replace("[", "&#91;"). \
            replace("]", "&#93;").replace(",", "&#44;")
    else:
        return text.replace("&", "&amp;").replace("[", "&#91;"). \
            replace("]", "&#93;")


# 文本
class Text:
    def __init__(self, text: str) -> None:
        self.text = cq_encode(text)
        self.raw_text = text
        self.content = {"type": "text", "data": {"text": self.raw_text}}

    def set(self, text: str) -> None:
        self.text = cq_encode(text)
        self.raw_text = text
        self.content = {"type": "text", "data": {"text": self.raw_text}}

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

    def get(self) -> dict:
        return self.content

    def __str__(self) -> str:
        return "[CQ:face,id={}]".format(self.id)

    def __repr__(self) -> str:
        return str(self.content)


# 语音
class Record:
    def __init__(self, file: str, magic: bool | int = 0, cache: bool | int = True, proxy: bool | int = 1,
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
    def __init__(self, qq: int | str) -> None:
        if isinstance(qq, str) and qq != "all":
            raise ValueError("QQ号只能为数字或all")
        self.qq = qq
        self.content = {"type": "at", "data": {"qq": self.qq}}

    def set(self, qq: int) -> None:
        self.qq = qq
        self.content = {"type": "at", "data": {"qq": self.qq}}

    def get(self) -> dict:
        return self.content

    def __str__(self) -> str:
        return "[CQ:at,qq={}]".format(self.qq)

    def __repr__(self) -> str:
        return str(self.content)


class Image:
    def __init__(self, file: str, image_type: str = "", cache: bool | int = True) -> None:
        self.file = file
        self.type = image_type
        self.cache = cache
        if self.type != "" and self.type != "flash":
            raise ValueError("未知的图片类型")

        self.content = {"type": "image", "data": {"file": file}}
        if self.type != "":
            self.content["data"]["type"] = image_type

        if not self.cache:
            self.content["data"]["cache"] = 0

    def set(self, file: str) -> None:
        self.file = file
        self.content["data"]["file"] = file

    def get(self) -> dict:
        return self.content

    def __str__(self) -> str:
        cq = "[CQ:image,file={}".format(self.file)
        if self.type != "":
            cq += ",type={}"

        if not self.cache:
            cq += ",cache=0"

        return cq + "]"

    def __repr__(self):
        return str(self.content)


class Reply:
    def __init__(self, reply_id: int) -> None:
        self.id = reply_id
        self.content = {"type": "reply", "data": {"id": self.id}}

    def set(self, reply_id: int) -> None:
        self.id = reply_id
        self.content = {"type": "reply", "data": {"id": self.id}}

    def get(self) -> dict:
        return self.content

    def __str__(self) -> str:
        return "[CQ:reply,id={}]".format(self.id)

    def __repr__(self) -> str:
        return str(self.content)


class QQRichText:
    def __init__(self, *rich):
        rich_text = ""
        rich_list = []

        if len(rich) == 1:
            rich = rich[0]

        if isinstance(rich, str):
            rich_text = rich
        elif isinstance(rich, list) or isinstance(rich, tuple):
            rich_list = list(rich)
        elif isinstance(rich, QQRichText):
            rich_list = rich.get()
        elif isinstance(rich, dict):
            rich_list.append(rich)
        else:
            try:
                rich_list.append(rich.get())
            except (TypeError, AttributeError):
                raise ValueError("参数类型错误，未知的rich类型")

        # 富文本解析
        if rich_text != "":
            self.rich_text = rich_text
            pattern = r"\[CQ:(\w+)(?:,([^\]]+))?\]"
            text = ""
            cq = ""
            flag = False
            for i in rich_text:
                if i == "[" and not flag:
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
                elif i == "]" and flag:
                    # CQ结束
                    cq += "]"
                    flag = False
                    rich = re.findall(pattern, cq)
                    if len(rich) > 0:
                        rich_data = cq_decode(rich[0][1], in_cq=True)
                        rich_list.append(
                            {
                                "type": rich[0][0],
                                "data": dict(  # CQ码参数
                                    cq_decode(x, in_cq=True)
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
                self.rich_list.append(Text(rich).get())
            elif isinstance(rich, QQRichText):
                self.rich_list += rich.get()
            else:
                try:
                    self.rich_list.append(rich.get())
                except (TypeError, AttributeError):
                    self.rich_list.append(rich)

    def __str__(self):
        self.rich_text = ""
        for rich in self.rich_list:
            if isinstance(rich, dict):
                if "type" not in rich or "data" not in rich:
                    raise ValueError("转换为CQ码时失败，未知的类型或是非标准message，无法转换")
                if rich["type"] == "text":
                    self.rich_text += rich["data"]["text"]
                else:
                    self.rich_text += "[CQ:{}".format(rich["type"])
                    if rich["data"]:
                        for rich_type, rich_data in rich["data"].items():
                            rich_type = cq_encode(rich_type, in_cq=True)
                            rich_data = cq_encode(rich_data, in_cq=True)
                            self.rich_text += ",{}={}".format(rich_type, rich_data)
                    self.rich_text += "]"
            elif isinstance(rich, str):
                self.rich_text += rich
            else:
                try:
                    self.rich_text += str(QQRichText(rich.get()))
                except (TypeError, AttributeError):
                    raise ValueError("转换为CQ码时失败，未知的变量类型，无法转换")

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
            except (TypeError, AttributeError):
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
            except (TypeError, AttributeError):
                return False


# 单元测试
if __name__ == "__main__":
    b = Face(1)

    c = QQRichText([
        Text("Hi"),
        Face(1),
        Record("https://gchat.qpic.cn/gchatpic_new/100000/100000/100000/0?term=2", False),
    ])
    print(b)
    print(c)
    print(b in c)

    print(
        str(
            QQRichText(
                [{'type': 'text', 'data': {'text': 'test'}}]
            )
        )
    )

    print(
        str(
            QQRichText(
                "test"
            )
        )
    )
