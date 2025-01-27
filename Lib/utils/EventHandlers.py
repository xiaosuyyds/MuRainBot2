"""
事件处理器
"""

from Lib.core import EventManager, ConfigManager
from Lib.utils import EventClassifier, Logger, QQRichText

import inspect
from typing import Literal, Callable, Any, Type

logger = Logger.get_logger()


class Rule:
    """
    Rule基类，请勿直接使用
    """

    def match(self, event_data: EventClassifier.Event):
        """
        匹配事件
        @param event_data: 事件数据
        @return: 是否匹配到事件
        """
        pass


class KeyValueRule(Rule):
    """
    键值规则
    """
    def __init__(self, key, value, model: Literal["eq", "ne", "in", "not in", "func"],
                 func: Callable[[Any, Any], bool] = None):
        self.key = key
        self.value = value
        self.model = model
        if model == "func" and func is None:
            raise ValueError("if model is func, func must be a callable")
        self.func = func

    def match(self, event_data: EventClassifier.Event):
        try:
            match self.model:
                case "eq":
                    return event_data.get(self.key) == self.value
                case "ne":
                    return event_data.get(self.key) != self.value
                case "in":
                    return self.value in event_data.get(self.key)
                case "not in":
                    return self.value not in event_data.get(self.key)
                case "func":
                    return self.func(event_data.get(self.key), self.value)
        except Exception as e:
            logger.error(f"Error occurred while matching event {event_data}: {repr(e)}")
            return False


class FuncRule(Rule):
    """
    函数规则
    """
    def __init__(self, func):
        self.func = func

    def match(self, event_data: EventClassifier.Event):
        try:
            return self.func(event_data)
        except Exception as e:
            logger.error(f"Error occurred while matching event {event_data}: {repr(e)}")
            return False


class CommandRule(Rule):
    """
    命令规则
    """
    def __init__(self, command: str, aliases: set[str] = None, command_start: list[str] = None):
        if aliases is None:
            aliases = set()
        if command_start is None:
            command_start = ConfigManager.GlobalConfig().command.command_start
        if any(_ in command for _ in ['[', ']'] + command_start):
            raise ValueError("command cannot contain [ or ]")
        if command in aliases:
            raise ValueError("command cannot be an alias")

        self.command = command
        self.aliases = aliases
        self.command_start = command_start

    def match(self, event_data: EventClassifier.MessageEvent):
        if not isinstance(event_data, EventClassifier.MessageEvent):
            logger.warning(f"event {event_data} is not a MessageEvent, cannot match command")
            return False

        flag = False
        segments = event_data.message.rich_array
        if (
                len(segments) > 0 and
                isinstance(segments[0], QQRichText.At) and
                int(segments[0].data.get("qq")) == event_data.self_id
        ):
            segments = segments[1:]
            flag = True
        message = str(QQRichText.QQRichText(segments))
        while len(message) > 0 and message[0] == " ":
            message = message[1:]

        message = QQRichText.QQRichText(message)
        string_message = str(message)
        commands = [_ + self.command for _ in self.command_start]
        if flag:
            # 如果消息前面有at，则不需要命令起始符
            commands += [self.command] + [alias for alias in self.aliases]

        commands += [_ + alias for alias in self.aliases for _ in self.command_start]

        if any(string_message.startswith(_) for _ in commands):
            for start in self.command_start:
                if string_message.startswith(start):
                    string_message = string_message[len(start):]
                    break
            for alias in self.aliases:
                if string_message.startswith(alias):
                    string_message = self.command + string_message[len(alias):]
                    break
            message = QQRichText.QQRichText(string_message)
            event_data.message = message
            event_data.raw_message = string_message
            return True
        return False


def _to_me(event_data: EventClassifier.MessageEvent):
    """
    判断是否是@自己或是私聊
    @param event_data: 事件数据
    @return: 是否是@自己或是私聊
    """
    if not isinstance(event_data, EventClassifier.MessageEvent):
        logger.warning(f"event {event_data} is not a MessageEvent, cannot match to_me")
        return False
    if isinstance(event_data, EventClassifier.PrivateMessageEvent):
        return True
    if isinstance(event_data, EventClassifier.GroupMessageEvent):
        for rich in event_data.message.rich_array:
            if isinstance(rich, QQRichText.At) and int(rich.data.get("qq")) == event_data.self_id:
                return True
    return False


to_me = FuncRule(_to_me)


class Matcher:
    """
    事件处理器
    """
    def __init__(self):
        self.handlers = []

    def register_handler(self, priority: int = 0, rules: list[Rule] = None, *args, **kwargs):
        """
        注册事件处理器
        @param priority: 事件优先级
        @param rules: 匹配规则
        """
        if rules is None:
            rules = []
        if any(not isinstance(rule, Rule) for rule in rules):
            raise TypeError("rules must be a list of Rule")

        def wrapper(func):
            self.handlers.append((priority, rules, func, args, kwargs))
            return func

        return wrapper

    def match(self, event_data: EventClassifier.Event):
        """
        匹配事件处理器
        @param event_data: 事件数据
        """
        for priority, rules, handler, args, kwargs in sorted(self.handlers, key=lambda x: x[0], reverse=True):
            try:
                if all(rule.match(event_data) for rule in rules):
                    handler(event_data, *args, **kwargs)
            except Exception as e:
                logger.error(f"Error occurred while matching event {event_data}: {repr(e)}")


events_matchers: dict[str, dict[Type[EventClassifier.Event], list[tuple[int, list[Rule], Matcher]]]] = {}


def _on_event(event_data, path, event_type):
    matchers = events_matchers[path][event_type]
    for priority, rules, matcher in sorted(matchers, key=lambda x: x[0], reverse=True):
        if all(rule.match(event_data) for rule in rules):
            matcher.match(event_data)


def on_event(event: Type[EventClassifier.Event], priority: int = 0, rules: list[Rule] = None):
    """
    注册事件处理器
    @param event: 事件类型
    @param priority: 事件优先级
    @param rules: 匹配规则
    @return: 事件处理器
    """
    if rules is None:
        rules = []
    if any(not isinstance(rule, Rule) for rule in rules):
        raise TypeError("rules must be a list of Rule")
    if not issubclass(event, EventClassifier.Event):
        raise TypeError("event must be an instance of EventClassifier.Event")
    path = inspect.stack()[1].filename
    if path not in events_matchers:
        events_matchers[path] = {}
    if event not in events_matchers[path]:
        events_matchers[path][event] = []
        EventManager.event_listener(event, path=path, event_type=event)(_on_event)
    events_matcher = Matcher()
    events_matchers[path][event].append((priority, rules, events_matcher))
    return events_matcher
