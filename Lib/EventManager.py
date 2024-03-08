# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

import threading


def cmp(x):
    return x[2]


register_list = []  # event_type, func, arg, args


def register_event(event_type: [str, str], func, arg: int = 0, *args):
    """
    注册事件
    :param event_type: 接收的事件类型，可以是一个字符串，也可以是一个列表，列表中的字符串会依次匹配
    :param func: 接收的函数
    :param arg: 优先级，默认0
    :param args: 传给func的参数
    :return: None
    """
    if args is None:
        args = []
    register_list.append((event_type, func, arg, args))
    register_list.sort(key=cmp, reverse=True)


class Event:
    """
    Event——广播事件

    event_type: 事件类型，可以是一个字符串，也可以是一个列表，列表中的字符串会依次匹配
    event_data: 事件数据
    """

    def __init__(self, event_type: [str, str], event_data):
        self.event_class = event_type
        self.event_data = event_data
        for event_class, func, arg, args in register_list:
            if event_class == self.event_class or event_class == ["", ""] or event_class == "":
                threading.Thread(target=lambda: func(self.event_class, self.event_data, *args)).start()


# 单元测试
if __name__ == '__main__':
    def test_func(type_, arg):
        print(1, type_, arg)


    def test_func2(type_, arg, num=2):
        print(num, type_, arg)


    register_event('test', test_func, 1)
    register_event('', test_func2, 2)
    register_event('test', test_func, 1)

    Event('test', 'data')
