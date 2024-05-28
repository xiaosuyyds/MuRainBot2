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


class QQRichText:

    def __init__(self, *rich):
        self.rich = rich

        # 特判
        if len(self.rich) == 1:
            self.rich = self.rich[0]

        # 识别输入的是CQCode or json形式的富文本
        # 如果输入的是CQCode，则转换为json形式的富文本

        # 处理CQCode
        if isinstance(self.rich, str):
            self.rich_text = self.rich
            self.rich = []
            # 匹配CQ码或纯文本（纯文本不含[]，利用这一点区分CQ码和纯文本）
            pattern = r"\[CQ:(\w+)(?:,([^\]]+))?\]|([^[\]]+)"

            # 匹配CQCode
            list_ = re.findall(pattern, self.rich_text)
            # 处理CQ码
            for rich in list_:
                # CQ码的结果类似('at', 'qq=114514', '')，而纯文本类似('', '', ' -  &#91;x&#93; 使用 `&amp;data` 获取地址')
                # 检测第一个值是否为空字符串即可区分

                if rich[0]:  # CQ码
                    self.rich.append({
                        "type": rich[0],  # CQ码类型
                        "data": dict(  # CQ码参数
                            cq_decode(x, in_cq=True)
                            .split("=", 1) for x in rich[1].split(",")
                        ) if rich[1] else {},
                    })
                else:  # 纯文本
                    self.rich.append({
                        "type": "text",
                        "data": cq_decode(rich[2])
                    })

        elif isinstance(self.rich, dict):
            self.rich = [self.rich]

        else:
            raise TypeError("QQRichText: 输入类型错误")

    def __str__(self):
        # 将json形式的富文本转换为CQ码
        self.rich_text = ""
        for rich in self.rich:
            # 纯文本
            if rich.get("type") == "text":
                self.rich_text += cq_encode(rich.get("data"))
            # CQ码
            else:
                self.rich_text += "[CQ:" + rich.get("type") + "," + ",".join(
                    [cq_encode(x, in_cq=True) + "=" + cq_encode(rich.get("data")[x], in_cq=True)
                     for x in rich.get("data").keys()]) + "]"
        return self.rich_text

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, index):
        return self.rich[index]

    def __add__(self, other):
        other = QQRichText(other)
        return self.rich + other.rich

    def __eq__(self, other):
        other = QQRichText(other)

        return self.rich == other.rich

    def __contains__(self, other):
        if isinstance(other, QQRichText):
            return all(item in self.rich for item in other.rich)
        else:
            try:
                return str(other) in str(self)
            except (TypeError, AttributeError):
                return False


# 单元测试
if __name__ == "__main__":
    # 测试CQ解码
    print(cq_decode(" - &#91;x&#93; 使用 `&amp;data` 获取地址"))

    # 测试CQ编码
    print(cq_encode(" - [x] 使用 `&data` 获取地址"))

    # 测试QQRichText
    rich = QQRichText(
        "[CQ:share,title=标题,url=https://baidu.com] [CQ:at,qq=1919810] -  &#91;x&#93; 使用 `&amp;data` 获取地址")
    print(rich.rich)
    print(rich)
