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
        pass


class KeyValueRule(Rule):
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
    def __init__(self, func):
        self.func = func

    def match(self, event_data: EventClassifier.Event):
        try:
            return self.func(event_data)
        except Exception as e:
            logger.error(f"Error occurred while matching event {event_data}: {repr(e)}")
            return False


class CommandRule(Rule):
    def __init__(self, command: str, aliases: set[str] = None):
        if aliases is None:
            aliases = set()
        if any(_ in command for _ in ['[', ']']):
            raise ValueError("command cannot contain [ or ]")
        if command in aliases:
            raise ValueError("command cannot be an alias")
        self.command = command
        self.aliases = aliases

    def match(self, event_data: EventClassifier.MessageEvent):
        if not isinstance(event_data, EventClassifier.MessageEvent):
            logger.warning(f"event {event_data} is not a MessageEvent, cannot match command")

        segments = event_data.message.rich_array
        if isinstance(segments[0], QQRichText.At) and int(segments[0].data.get("qq")) == event_data.self_id:
            segments = segments[1:]
        message = str(QQRichText.QQRichText(segments))
        while len(message) > 0 and message[0] == " ":
            message = message[1:]
        for _ in ConfigManager.GlobalConfig().command.command_start:
            if message.startswith(_):
                if len(_) > 0:
                    message = message[len(_):]
                break

        message = QQRichText.QQRichText(message)
        string_message = str(message)
        if string_message.startswith(self.command) or any(string_message.startswith(alias) for alias in self.aliases):
            event_data.message = message
            event_data.raw_message = string_message
            return True
        return False


def _to_me(event_data: EventClassifier.MessageEvent):
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
    def __init__(self):
        self.handlers = []

    def register_handler(self, priority: int = 0, rules: list[Rule] = None, *args, **kwargs):
        if rules is None:
            rules = []
        if any(not isinstance(rule, Rule) for rule in rules):
            raise TypeError("rules must be a list of Rule")

        def wrapper(func):
            self.handlers.append((priority, rules, func, args, kwargs))
            return func

        return wrapper

    def match(self, event_data: EventClassifier.Event):
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
