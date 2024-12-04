#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

"""
QQRichText
QQ富文本处理
"""

import inspect
import re
import Lib.OnebotAPI as OnebotAPI
import Lib.QQDataCacher as QQDataCacher
import Lib.core.Logger as Logger


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


def cq_2_array(cq: str) -> list:
    if not isinstance(cq, str):
        raise TypeError("cq_2_array: 输入类型错误")

    # 匹配CQ码或纯文本（纯文本不含[]，利用这一点区分CQ码和纯文本）
    pattern = r"\[CQ:(\w+)(?:,([^\]]+))?\]|([^[\]]+)"

    # 匹配CQCode
    list_ = re.findall(pattern, cq)
    cq_array = []
    # 处理CQ码
    for rich in list_:
        # CQ码的结果类似('at', 'qq=114514', '')，而纯文本类似('', '', ' -  &#91;x&#93; 使用 `&amp;data` 获取地址')
        # 检测第一个值是否为空字符串即可区分

        if rich[0]:  # CQ码
            cq_array.append({
                "type": rich[0],  # CQ码类型
                "data": dict(
                    map(
                        lambda x: cq_decode(x, in_cq=True).split("=", 1),
                        rich[1].split(",")
                    )
                ) if rich[1] else {},
            })
        else:  # 纯文本
            cq_array.append({
                "type": "text",
                "data": {
                    "text": cq_decode(rich[2])
                }
            })
    return cq_array


def array_2_cq(cq_array: list | dict) -> str:
    # 特判
    if isinstance(cq_array, dict):
        cq_array = [cq_array]

    if not isinstance(cq_array, (list, tuple)):
        raise TypeError("array_2_cq: 输入类型错误")

    # 将json形式的富文本转换为CQ码
    text = ""
    for segment in cq_array:
        # 纯文本
        if segment.get("type") == "text":
            text += cq_encode(segment.get("data").get("text"))
        # CQ码
        else:
            if segment.get("data"):  # 特判
                text += f"[CQ:{segment.get('type')}," + ",".join(
                    [cq_encode(x, in_cq=True) + "=" + cq_encode(segment.get("data")[x], in_cq=True)
                     for x in segment.get("data").keys()]) + "]"
            else:
                text += f"[CQ:{segment.get('type')}]"
    return text


segments = []
segments_map = {}


class Meta(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        if 'Segment' in globals() and issubclass(cls, Segment):
            segments.append(cls)  # 将子类添加到全局列表中
            segments_map[cls.segment_type] = cls


class Segment(metaclass=Meta):
    segment_type = None

    def __init__(self, cq):
        self.cq = cq
        if isinstance(cq, str):
            self.array = cq_2_array(cq)[0]
            self.type, self.data = list(self.array.values())
        elif isinstance(cq, dict):
            self.array = cq
            self.cq = array_2_cq(self.array)
            self.type, self.data = list(self.array.values())
        else:
            for segment in segments:
                if isinstance(cq, segment):
                    self.array = cq.array
                    self.cq = str(self.cq)
                    # print(self.array.values(), list(self.array.values()))
                    self.type, self.data = list(self.array.values())
                    break
            else:
                # print(cq, str(cq), type(cq))
                raise TypeError("Segment: 输入类型错误")

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        self.cq = array_2_cq(self.array)
        return self.cq

    def __setitem__(self, key, value):
        self.array[key] = value

    def __getitem__(self, key):
        return self.array.get(key)

    def get(self, *args, **kwargs):
        return self.array.get(*args, **kwargs)

    def __delitem__(self, key):
        del self.array[key]

    def __eq__(self, other):
        other = Segment(other)
        return self.array == other.array

    def __contains__(self, other):
        if isinstance(other, Segment):
            return all(item in self.array for item in other.array)
        else:
            try:
                return str(other) in str(self)
            except (TypeError, AttributeError):
                return False

    def render(self, group_id: int | None = None):
        return f"[{self.array.get('type', 'unknown')}: {self.cq}]"

    def set_data(self, k, v):
        self.array["data"][k] = v


segments.append(Segment)


class Text(Segment):
    segment_type = "text"

    def __init__(self, text):
        super().__init__(text)
        self.text = self["data"]["text"] = text

    def __add__(self, other):
        other = Text(other)
        return self.text + other.text

    def __eq__(self, other):
        other = Text(other)
        return self.text == other.text

    def __contains__(self, other):
        if isinstance(other, Text):
            return other.text in self.text
        else:
            try:
                return str(other) in str(self.text)
            except (TypeError, AttributeError):
                return False

    def set_text(self, text):
        self.text = text
        self["data"]["text"] = text

    def render(self, group_id: int | None = None):
        return self.text


class Face(Segment):
    segment_type = "face"

    def __init__(self, face_id):
        self.face_id = face_id
        super().__init__({"type": "face", "data": {"id": str(face_id)}})

    def set_id(self, face_id):
        self.face_id = face_id
        self.array["data"]["id"] = str(face_id)

    def render(self, group_id: int | None = None):
        return "[表情: %s]" % self.face_id


class At(Segment):
    segment_type = "at"

    def __init__(self, qq):
        self.qq = qq
        super().__init__({"type": "at", "data": {"qq": str(qq)}})

    def set_id(self, qq_id):
        self.qq = qq_id
        self.array["data"]["qq"] = str(qq_id)

    def render(self, group_id: int | None = None):
        if group_id:
            return f"@{QQDataCacher.get_group_user_data(group_id, self.qq).nickname}: {self.qq}"
        else:
            return f"@{QQDataCacher.get_user_data(self.qq).nickname}: {self.qq}"


class Image(Segment):
    segment_type = "image"

    def __init__(self, file):
        self.file = file
        super().__init__({"type": "image", "data": {"file": str(file)}})

    def set_file(self, file):
        self.file = file
        self.array["data"]["file"] = str(file)

    def render(self, group_id: int | None = None):
        return "[图片: %s]" % self.file


class Record(Segment):
    segment_type = "record"

    def __init__(self, file):
        self.file = file
        super().__init__({"type": "record", "data": {"file": str(file)}})

    def set_file(self, file):
        self.file = file
        self.array["data"]["file"] = str(file)

    def render(self, group_id: int | None = None):
        return "[语音: %s]" % self.file


class Video(Segment):
    segment_type = "video"

    def __init__(self, file):
        self.file = file
        super().__init__({"type": "video", "data": {"file": str(file)}})

    def set_file(self, file):
        self.file = file
        self.array["data"]["file"] = str(file)

    def render(self, group_id: int | None = None):
        return f"[视频: {self.file}]"


class Rps(Segment):
    segment_type = "rps"

    def __init__(self):
        super().__init__({"type": "rps"})


class Dice(Segment):
    segment_type = "dice"

    def __init__(self):
        super().__init__({"type": "dice"})


class Shake(Segment):
    segment_type = "shake"

    def __init__(self):
        super().__init__({"type": "shake"})


# 戳一戳（未完全实现）
class Poke(Segment):
    segment_type = "poke"

    def __init__(self, type_):
        self.type = type_
        super().__init__({"type": "poke", "data": {"type": str(self.type)}})

    def set_type(self, qq_type):
        self.type = qq_type
        self.array["data"]["type"] = str(qq_type)


class Anonymous(Segment):
    segment_type = "anonymous"

    def __init__(self, ignore=False):
        self.ignore = 0 if ignore else 1
        super().__init__({"type": "anonymous", "data": {"ignore": str(self.ignore)}})

    def set_ignore(self, ignore):
        self.ignore = 0 if ignore else 1
        self.array["data"]["ignore"] = str(self.ignore)


class Share(Segment):
    segment_type = "share"

    def __init__(self, url, title, content="", image=""):
        self.url = url
        self.title = title
        self.content = content
        self.image = image
        super().__init__({"type": "share", "data": {"url": str(self.url), "title": str(self.title)}})

        if content != "":
            self.array["data"]["content"] = str(self.content)

        if image != "":
            self.array["data"]["image"] = str(self.image)

    def set_url(self, url):
        self.array["data"]["url"] = str(url)
        self.url = url

    def set_title(self, title):
        self.title = title
        self.array["data"]["title"] = str(title)

    def set_content(self, content):
        self.content = content
        self.array["data"]["content"] = str(content)

    def set_image(self, image):
        self.image = image
        self.array["data"]["image"] = str(image)


class Contact(Segment):
    segment_type = "contact"

    def __init__(self, type_, id_):
        self.type = type_
        self.id = id_
        super().__init__({"type": "contact", "data": {"type": str(self.type), "id": str(self.id)}})

    def set_type(self, type_):
        self.type = type_
        self.array["data"]["type"] = str(type_)

    def set_id(self, id_):
        self.id = id_
        self.array["data"]["id"] = str(id_)


class Location(Segment):
    segment_type = "location"

    def __init__(self, lat, lon, title="", content=""):
        self.lat = lat
        self.lon = lon
        self.title = title
        self.content = content
        super().__init__({"type": "location", "data": {"lat": str(self.lat), "lon": str(self.lon)}})

        if title != "":
            self.array["data"]["title"] = str(self.title)

        if content != "":
            self.array["data"]["content"] = str(self.content)

    def set_lat(self, lat):
        self.lat = lat
        self.array["data"]["lat"] = str(lat)

    def set_lon(self, lon):
        self.lon = lon
        self.array["data"]["lon"] = str(lon)


class Node(Segment):
    segment_type = "node"

    def __init__(self, name: str, uid: int, message, message_id: int = None):
        if message_id is None:
            self.name = name
            self.user_id = uid
            self.message = QQRichText(message).get_array()
            super().__init__({"type": "node", "data": {"nickname": str(self.name), "user_id": str(self.user_id), "content": self.message}})
        else:
            self.message_id = message_id
            super().__init__({"type": "node", "data": {"id": str(message_id)}})

    def set_message(self, message):
        self.message = message

    def set_name(self, name):
        self.name = name
        self.array["data"]["name"] = str(name)

    def set_uid(self, uid):
        self.uid = uid
        self.array["data"]["uin"] = str(uid)

    def render(self, group_id: int | None = None):
        if self.message_id is not None:
            return f"[合并转发节点: {self.name}({self.uid}): {self.message}]"
        else:
            return f"[合并转发节点: {self.message_id}]"


class Music(Segment):
    segment_type = "music"

    def __init__(self, type_, id_):
        self.type = type_
        self.id = id_
        super().__init__({"type": "music", "data": {"type": str(self.type), "id": str(self.id)}})

    def set_type(self, type_):
        self.type = type_
        self.array["data"]["type"] = str(type_)

    def set_id(self, id_):
        self.id = id_
        self.array["data"]["id"] = str(id_)


class CustomizeMusic(Segment):
    segment_type = "music"

    def __init__(self, url, audio, image, title, content):
        self.url = url
        self.audio = audio
        self.image = image
        self.title = title
        self.content = content
        super().__init__({"type": "music", "data": {"type": "custom", "url": str(self.url), "audio": str(self.audio),
                                                    "image": str(self.image), "title": str(self.title),
                                                    "content": str(self.content)}})

    def set_url(self, url):
        self.url = url
        self.array["data"]["url"] = str(url)

    def set_audio(self, audio):
        self.audio = audio
        self.array["data"]["audio"] = str(audio)

    def set_image(self, image):
        self.image = image
        self.array["data"]["image"] = str(image)

    def set_title(self, title):
        self.title = title
        self.array["data"]["title"] = str(title)

    def set_content(self, content):
        self.content = content
        self.array["data"]["content"] = str(content)


class Reply(Segment):
    segment_type = "reply"

    def __init__(self, message_id):
        self.message_id = message_id
        super().__init__({"type": "reply", "data": {"id": str(self.message_id)}})

    def set_message_id(self, message_id):
        self.message_id = message_id
        self.array["data"]["id"] = str(self.message_id)

    def render(self, group_id: int | None = None):
        return f"[回复: {self.message_id}]"


class Forward(Segment):
    segment_type = "forward"

    def __init__(self, forward_id):
        self.forward_id = forward_id
        super().__init__({"type": "forward", "data": {"id": str(self.forward_id)}})

    def set_forward_id(self, forward_id):
        self.forward_id = forward_id
        self.array["data"]["id"] = str(self.forward_id)

    def render(self, group_id: int | None = None):
        return f"[合并转发: {self.forward_id}]"


# 并不是很想写这个东西.png
# class CustomizeForward(Segment):
#     def __init__(self, title, content, source):
#         self.title = title
#         self.content = content
#         self.source = source
#         super().__init__({"type": "forward", "data": {"title": str(self.title)
#         , "content": str(self.content), "source": str(self.source)}})
#
#     def set_title(self, title):
#         self.array["data"]["title"] = str(self.title)
#         self.title = title
#
#     def set_content(self, content):


class XML(Segment):
    segment_type = "xml"

    def __init__(self, xml):
        self.xml = xml
        super().__init__({"type": "xml", "data": {"xml": str(self.xml)}})

    def set_xml(self, xml):
        self.xml = xml
        self.array["data"]["xml"] = str(self.xml)


class JSON(Segment):
    segment_type = "json"

    def __init__(self, data):
        self.data = data
        super().__init__({"type": "json", "data": {"json": str(self.data)}})

    def set_json(self, data):
        self.data = data
        self.array["data"]["json"] = str(self.data)


class QQRichText:

    def __init__(self, *rich: str | dict | list | tuple | Segment):

        # 特判
        self.rich_array: list[Segment] = []
        if len(rich) == 1:
            rich = rich[0]

        # 识别输入的是CQCode or json形式的富文本
        # 如果输入的是CQCode，则转换为json形式的富文本

        # 处理CQCode
        if isinstance(rich, str):
            rich_string = rich
            rich = cq_2_array(rich_string)

        elif isinstance(rich, dict):
            rich = [rich]
        elif isinstance(rich, (list, tuple)):
            array = []
            for item in rich:
                if isinstance(item, dict):
                    array.append(item)
                elif isinstance(item, str):
                    array += cq_2_array(item)
                else:
                    for segment in segments:
                        if isinstance(item, segment):
                            array.append(item.array)
                            break
                    else:
                        if isinstance(rich, QQRichText):
                            array += rich.rich_array
                        else:
                            raise TypeError("QQRichText: 输入类型错误")
            rich = array
        else:
            for segment in segments:
                if isinstance(rich, segment):
                    rich = [rich.array]
                    break
            else:
                if isinstance(rich, QQRichText):
                    rich = rich.rich_array
                else:
                    raise TypeError("QQRichText: 输入类型错误")

        # 将rich转换为的Segment
        for _ in range(len(rich)):
            if rich[_]["type"] in segments_map:
                try:
                    params = inspect.signature(segments_map[rich[_]["type"]]).parameters
                    kwargs = {}
                    for param in params:
                        if param in rich[_]["data"]:
                            kwargs[param] = rich[_]["data"][param]
                        else:
                            if rich[_]["type"] == "reply" and param == "message_id":
                                kwargs[param] = rich[_]["data"].get("id")
                            elif rich[_]["type"] == "face" and param == "face_id":
                                kwargs[param] = rich[_]["data"].get("id")
                            elif rich[_]["type"] == "forward" and param == "forward_id":
                                kwargs[param] = rich[_]["data"].get("id")
                            else:
                                if params[param].default != params[param].empty:
                                    kwargs[param] = params[param].default
                    segment = segments_map[rich[_]["type"]](**kwargs)
                    # 检查原cq中是否含有不在segment的data中的参数
                    for k, v in rich[_]["data"].items():
                        if k not in segment["data"]:
                            segment.set_data(k, v)
                    rich[_] = segment
                except Exception as e:
                    Logger.logger.warning(f"转换{rich[_]}时失败，报错信息: {repr(e)}")
                    rich[_] = Segment(rich[_])
            else:
                rich[_] = Segment(rich[_])

        self.rich_array: list[Segment] = rich

    def render(self, group_id: int | None = None):
        # 渲染成类似: abc123[图片:<URL>]@xxxx[uid]
        text = ""
        for rich in self.rich_array:
            text += rich.render(group_id=group_id)
        return text

    def __str__(self):
        self.rich_string = array_2_cq(self.rich_array)
        return self.rich_string

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, index):
        return self.rich_array[index]

    def __add__(self, other):
        other = QQRichText(other)
        return self.rich_array + other.rich_array

    def __eq__(self, other):
        other = QQRichText(other)

        return self.rich_array == other.rich_array

    def __contains__(self, other):
        if isinstance(other, QQRichText):
            return all(item in self.rich_array for item in other.rich_array)
        else:
            try:
                return str(other) in str(self)
            except (TypeError, AttributeError):
                return False

    def send(self, user_id=-1, group_id=-1):
        OnebotAPI.OnebotAPI().send_msg(user_id=user_id, group_id=group_id, message=str(self))

    def get_array(self):
        return [array.array for array in self.rich_array]


# 单元测试
if __name__ == "__main__":
    # 测试CQ解码
    print(cq_decode(" - &#91;x&#93; 使用 `&amp;data` 获取地址"))

    # 测试CQ编码
    print(cq_encode(" - [x] 使用 `&data` 获取地址"))

    # 测试QQRichText
    rich = QQRichText(
        "[CQ:reply,id=123][CQ:share,title=标题,url=https://baidu.com] [CQ:at,qq=1919810,abc=123] -  &#91;x&#93; 使用 "
        " `&amp;data` 获取地址")
    print(rich.rich_array)
    print(rich)
    print(rich.render())

    print(QQRichText(At(114514)))
    print(Segment(At(1919810)))
    print(QQRichText([{"type": "text", "data": {"text": "1919810"}}]))
