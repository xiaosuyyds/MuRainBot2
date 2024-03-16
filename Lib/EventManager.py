# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

import threading
import traceback
import re
from typing import Callable, Any, Tuple, Dict

register_event_list = []  # event_type, func, arg, args, kwargs, by_file
register_keyword_list = []  # keyword, func, arg, args, kwargs, by_file


def register_event(event_type: tuple[str, str] | str | tuple[tuple[str, str] | str], arg: int = 0) -> Callable:
    """
    注册事件，需要使用装饰器语法
    :param event_type: 接收的事件类型，可以是一个字符串，也可以是一个列表，列表中的字符串会依次匹配，例如：
    ('message', 'group') 或者 'message'，若为"all"或"*"则代表匹配所有事件
    :param arg: 优先级，默认0
    :return: None
    """

    def wrapper(func, *args, **kwargs):
        # print("运行run")
        # func(*args, **kwargs)
        # print("func运行结束")
        register_event_list.append((event_type, func, arg, args, kwargs, traceback.extract_stack()[-2].filename))
        register_event_list.sort(key=lambda x: x[2], reverse=True)

        return func

    return wrapper


def unregister_event(event_type: tuple[str, str] | str | tuple[tuple[str, str] | str]):
    """
    取消注册事件
    用于取消注册一个事件，取消注册后插件将不再对此事件做出响应
    :param event_type: 接收的事件类型，可以是一个字符串，也可以是一个列表，列表中的字符串会依次匹配，例如：
    ('message', 'group') 或者 'message'
    :return: None
    """
    for i in range(len(register_event_list)):
        if (register_event_list[i][0] == event_type and
                register_event_list[i][5] == traceback.extract_stack()[-2].filename):
            del register_event_list[i]


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
    register_keyword_list.append((keyword, func, model, arg, args, traceback.extract_stack()[-2].filename))
    register_keyword_list.sort(key=lambda x: x[2], reverse=True)
    return


def unregister_keyword(keyword: str):
    """
    注销关键字
    用于取消注册一个关键词，注销后关键词会被取消被用于匹配
    需要传入对应的关键词字符串来将其取消注册，无法取消注册不属于此插件的关键词
    :param keyword: 关键词
    :return: None
    """
    for i in range(len(register_keyword_list)):
        if (register_keyword_list[i][0] == keyword and
                register_event_list[i][4] == traceback.extract_stack()[-2].filename):
            del register_keyword_list[i]


class Event:
    """
    Event——广播事件

    event_type: 事件类型，可以是一个字符串，也可以是一个列表，列表中的字符串会依次匹配
    event_data: 事件数据
    """

    def __init__(self, event_type: tuple[str, str] | str | tuple[tuple[str, str] | str], event_data):
        self.event_class = event_type
        self.event_data = event_data

        if self.event_class == "all" or self.event_class == "*":
            raise ValueError("不能将all或是*设为事件，因为会发生冲突。")

        # 事件扫描
        for event_class, func, arg, args, kwargs, by_file in register_event_list:
            if event_class == self.event_class or event_class == "all" or event_class == "*":
                threading.Thread(target=lambda: func(self.event_class, self.event_data, *args, **kwargs)).start()

        # 关键词检测
        if self.event_class is list:
            if self.event_class[0] == "message":
                message = str(self.event_data["raw_message"])
                for keyword, func, model, arg, args, by_file in register_keyword_list:
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

    @register_event('test', 5)
    @register_event('test2', 1)
    def test_func(event_type, arg):
        print(1, event_type, arg)

    @register_event('all', 2)
    @register_event('all', -1)
    def test_func2(event_type, arg, num=2):
        print(num, event_type, arg)

    Event('test', 'data')
    Event('test2', 'data')
