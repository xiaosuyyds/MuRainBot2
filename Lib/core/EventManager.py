from typing import Type, Any, TypeVar

from collections.abc import Callable
from dataclasses import dataclass, field

from Lib.core.ThreadPool import async_task
from . import ConfigManager
from ..utils import Logger
import inspect


logger = Logger.get_logger()


# 定义基础事件类
class Event:
    def call(self):
        """
        按优先级顺序同步触发所有监听器
        """
        if self.__class__ in event_listeners:
            for listener in sorted(event_listeners[self.__class__], key=lambda i: i.priority, reverse=True):
                try:
                    listener.func(self, **listener.kwargs)
                except Exception as e:
                    logger.error(f"Error occurred in listener: {repr(e)}")
                    if ConfigManager.GlobalConfig().debug.enable:
                        raise e

    @async_task
    def call_async(self):
        """
        无需等待的异步按优先级顺序触发所有监听器
        """
        self.call()


# 定义事件
T = TypeVar('T', bound='Event')


# 定义事件监听器的数据类
@dataclass(order=True)
class EventListener:
    priority: int  # 优先级，默认为排序的依据
    func: Callable[[T, ...], Any]  # 监听器函数
    kwargs: dict[str, Any] = field(default_factory=dict)  # 附加参数

    def __post_init__(self):
        # 确保监听器函数至少有一个参数
        if len(inspect.signature(self.func).parameters) < 1:
            raise TypeError("The listener takes at least 1 parameter")


# 定义监听器的类型和存储
event_listeners: dict[type[T], list[EventListener]] = {}


# 装饰器，用于注册监听器
def event_listener(event_class: type[T], priority: int = 0, **kwargs):
    """
    用于注册监听器
    """
    if not issubclass(event_class, Event):
        raise TypeError("Event class must be a subclass of Event")

    def wrapper(func: Callable[[T, ...], Any]):
        # 注册事件监听器
        listener = EventListener(priority=priority, func=func, kwargs=kwargs)
        event_listeners.setdefault(event_class, []).append(listener)
        return func

    return wrapper


if __name__ == "__main__":
    # 示例：自定义事件
    class MyEvent(Event):
        def __init__(self, message):
            self.message = message


    # 监听器函数
    @event_listener(MyEvent, priority=10, other_message="priority is 10")
    @event_listener(MyEvent, priority=100, other_message="priority is 100")
    def on_my_event(event, other_message=""):
        print(f"Received event: {event.message}!", other_message)


    # 触发事件
    event = MyEvent("Hello, World")
    event.call()  # 输出: Received event: Hello, World!
