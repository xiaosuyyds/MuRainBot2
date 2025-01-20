from Lib.core import EventManager
from Lib.utils import EventClassifier, Logger

import inspect
from typing import Literal, Callable, Any, Type

logger = Logger.get_logger()


class Rule:
    pass


class KeyValueRule(Rule):
    def __init__(self, key, value, model: Literal["eq", "ne", "in", "not in", "func"],
                 func: Callable[[Any, Any], bool] = None):
        self.key = key
        self.value = value
        self.model = model
        if model == "func" and func is None:
            raise ValueError("func must be a callable")
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


class Matcher:
    def __init__(self):
        self.handlers = []

    def register_handler(self, priority: int = 0, rules: list = None, *args, **kwargs):
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


events_matchers = {}


def _on_event(event_data, path, event_type):
    matchers = events_matchers[path][event_type]
    for priority, rules, matcher in sorted(matchers, key=lambda x: x[0], reverse=True):
        if all(rule.match(event_data) for rule in rules):
            matcher.match(event_data)


def on_event(event: Type[EventClassifier.Event], priority: int = 0, rules: list = None):
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
