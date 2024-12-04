import inspect

event_listeners = {}


# 基础事件类
class Event:
    def call(self):
        if self.__class__ in event_listeners:
            for listener in event_listeners[self.__class__]:
                listener(self)  # 通知所有监听器


# 装饰器，用于注册监听器
def event_listener(event_class):
    if event_class is None:
        raise TypeError("missing 1 required argument")
    if not issubclass(event_class, Event):
        raise TypeError("incorrect argument")

    def wrapper(func):
        # 确保监听器函数只接收一个参数
        if len(inspect.signature(func).parameters) != 1:
            raise TypeError("The listener takes 0 positional arguments but 1 will be given")
        event_listeners.setdefault(event_class, []).append(func)
        return func

    return wrapper


if __name__ == "__main__":
    # 示例：自定义事件
    class MyEvent(Event):
        def __init__(self, message):
            self.message = message


    # 监听器函数
    @event_listener(MyEvent)
    def on_my_event(event):
        print(f"Received event: {event.message}")


    # 触发事件
    event = MyEvent("Hello, World!")
    event.call()  # 输出: Received event: Hello, World!
