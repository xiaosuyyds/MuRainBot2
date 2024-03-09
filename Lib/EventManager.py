# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

import threading
import re

register_event_list = []  # event_type, func, arg, args
register_keyword_list = []  # keyword, func, arg, args


def register_event(event_type: tuple[str, str] | str | tuple[tuple[str, str] | str], func, arg: int = 0, *args) -> None:
    """
    注册事件
    :param event_type: 接收的事件类型，可以是一个字符串，也可以是一个列表，列表中的字符串会依次匹配，例如：
    ('message', 'group') 或者 'message'
    :param func: 接收的函数
    :param arg: 优先级，默认0
    :param args: 传给func的参数
    :return: None
    """

    if args is None:
        args = []
    if event_type is list:
        for event in event_type:
            if event is list:
                register_event_list.append((event, func, arg, args))
    register_event_list.append((event_type, func, arg, args))
    register_event_list.sort(key=lambda x: x[2], reverse=True)


def register_keyword(keyword: str, func, model: str = "INCLUDE", arg: int = 0, *args) -> None:
    """
    注册关键字
    :param keyword: 关键词
    :param func: 触发后调用的函数
    :param model: 匹配模式，支持BEGIN：仅当关键词位于消息开头时触发判定
                             END：仅当关键词位于消息末尾时触发判定
                             INCLUDE： 消息中只要包含关键词就触发判定
                             EXCLUDE： 消息中不包含关键词就触发判定
                             EQUAL： 消息与关键词完全匹配时触发判定
                             REGEX： 消息满足正则表达式时触发判定（此时关键词内容应为一个正则表达式）
                             默认INCLUDE
    :param arg: 优先级，默认0
    :param args: 传给func的参数
    :return: None
    """

    if args is None:
        args = []
    register_keyword_list.append((keyword, func, model, arg, args))
    register_keyword_list.sort(key=lambda x: x[2], reverse=True)
    return


class Event:
    """
    Event——广播事件

    event_type: 事件类型，可以是一个字符串，也可以是一个列表，列表中的字符串会依次匹配
    event_data: 事件数据
    """

    def __init__(self, event_type: tuple[str, str] | str | tuple[tuple[str, str] | str], event_data):
        self.event_class = event_type
        self.event_data = event_data
        # 事件扫描
        for event_class, func, arg, args in register_event_list:
            if event_class == self.event_class or event_class == ["", ""] or event_class == "":
                threading.Thread(target=lambda: func(self.event_class, self.event_data, *args)).start()

        # 关键词检测
        if self.event_class is list:
            if self.event_class[0] == "message":
                message = str(self.event_data["raw_message"])
                for keyword, func, model, arg, args in register_keyword_list:
                    if model == "BEGIN":
                        if message.startswith(keyword):
                            threading.Thread(target=lambda: func(self.event_class, self.event_data, *args)).start()
                    elif model == "END":
                        if message.endswith(keyword):
                            threading.Thread(target=lambda: func(self.event_class, self.event_data, *args)).start()
                    elif model == "INCLUDE":
                        if keyword in message:
                            threading.Thread(target=lambda: func(self.event_class, self.event_data, *args)).start()
                    elif model == "EXCLUDE":
                        if keyword not in message:
                            threading.Thread(target=lambda: func(self.event_class, self.event_data, *args)).start()
                    elif model == "EQUAL":
                        if message == keyword:
                            threading.Thread(target=lambda: func(self.event_class, self.event_data, *args)).start()
                    elif model == "REGEX":
                        if re.search(keyword, message):
                            threading.Thread(target=lambda: func(self.event_class, self.event_data, *args)).start()
                    else:
                        raise ValueError("Unsupported model: {}".format(model))


# 单元测试
if __name__ == '__main__':
    def test_func(event_type, arg):
        print(1, event_type, arg)


    def test_func2(event_type, arg, num=2):
        print(num, event_type, arg)


    register_event('test', test_func, 1)
    register_event('', test_func2, 2, 3)
    register_event('', test_func2, 2, 4)
    register_event('test', test_func, 1)

    Event('test', 'data')
    Event('test2', 'data')
