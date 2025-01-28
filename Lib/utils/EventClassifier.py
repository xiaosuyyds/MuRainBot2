"""
事件分发器
"""

from typing import TypedDict, NotRequired, Literal

from ..core import EventManager, ListenerServer
from . import QQRichText


class Event(EventManager.Event):
    """
    事件类
    """
    def __init__(self, event_data):
        self.event_data: dict = event_data
        self.time: int = self["time"]
        self.self_id: int = self["self_id"]
        self.post_type: str = self["post_type"]

    def __getitem__(self, item):
        if item not in self.event_data:
            raise KeyError(f"{item} not in {self.event_data}")
        return self.event_data.get(item)

    def get(self, key, default=None):
        """
        获取事件数据
        Args:
            key: 键
            default: 默认值
        Returns:
            None
        """
        return self.event_data.get(key, default)

    def __contains__(self, other):
        return other in self.event_data

    def __repr__(self):
        return str(self.event_data)


class EventData(TypedDict):
    """
    事件数据
    """
    cls: Event
    post_type: str
    rules: dict


events: list[EventData] = []


def register_event(post_type: str, **other_rules):
    """
    注册事件
    Args:
        post_type: 事件类型
        other_rules: 其他规则
    Returns:
        None
    """
    def decorator(cls):
        """
        Args:
            @param cls:
        Returns:
            None
        """
        data: EventData = {
            "cls": cls,
            "post_type": post_type,
            "rules": other_rules
        }
        events.append(data)
        return cls

    return decorator


class SenderDict(TypedDict, total=False):
    """
    发送者数据
    """
    user_id: NotRequired[int]
    nickname: NotRequired[str]
    sex: NotRequired[Literal["male", "female", "unknown"]]
    age: NotRequired[int]


class PrivateDict(TypedDict, total=False):
    """
    私聊发送者数据
    """
    user_id: NotRequired[int]
    nickname: NotRequired[str]
    sex: NotRequired[Literal["male", "female", "unknown"]]
    age: NotRequired[int]


class GroupSenderDict(TypedDict, total=False):
    """
    群聊发送者数据
    """
    user_id: NotRequired[int]
    nickname: NotRequired[str]
    card: NotRequired[str]
    sex: NotRequired[Literal["male", "female", "unknown"]]
    age: NotRequired[int]
    level: NotRequired[int]
    role: NotRequired[Literal["owner", "admin", "member"]]
    title: NotRequired[str]


# 注册事件类
@register_event("message")
class MessageEvent(Event):
    """
    消息事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.message_type = self["message_type"]
        self.user_id: int = int(self["user_id"])
        self.sub_type: str = self["sub_type"]
        self.message: QQRichText.QQRichText = QQRichText.QQRichText(self["message"])
        self.raw_message: str = self["raw_message"]
        self.message_id: int = int(self["message_id"])
        self.sender: SenderDict = self["sender"]


@register_event("message", message_type="private")
class PrivateMessageEvent(MessageEvent):
    """
    私聊消息事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.sender: PrivateDict = self["sender"]


@register_event("message", message_type="group")
class GroupMessageEvent(MessageEvent):
    """
    群聊消息事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.sender: GroupSenderDict = self["sender"]


@register_event("notice")
class NoticeEvent(Event):
    """
    通知事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.notice_type: str = self["notice_type"]


class FileDict(TypedDict, total=False):
    """
    文件数据
    """
    id: str
    name: str
    size: int
    busid: int


@register_event("notice", notice_type="group_upload")
class GroupUploadEvent(NoticeEvent):
    """
    群文件上传事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.file: FileDict = self["file"]


@register_event("notice", notice_type="group_admin")
class GroupAdminEvent(NoticeEvent):
    """
    群管理员变动事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.sub_type: str = self["sub_type"]


@register_event("notice", notice_type="group_admin", sub_type="set")
class GroupSetAdminEvent(GroupAdminEvent):
    """
    群管理员被设置事件
    """
    pass


@register_event("notice", notice_type="group_admin", sub_type="unset")
class GroupUnsetAdminEvent(GroupAdminEvent):
    """
    群管理员被取消事件
    """
    pass


@register_event("notice", notice_type="group_decrease")
class GroupDecreaseEvent(NoticeEvent):
    """
    群成员减少事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.operator_id = int(self["operator_id"])
        self.sub_type: str = self["sub_type"]


@register_event("notice", notice_type="group_decrease", sub_type="leave")
class GroupDecreaseLeaveEvent(GroupDecreaseEvent):
    """
    群成员离开事件
    """
    pass


@register_event("notice", notice_type="group_decrease", sub_type="kick")
class GroupDecreaseKickEvent(GroupDecreaseEvent):
    """
    群成员被踢事件
    """
    pass


@register_event("notice", notice_type="group_decrease", sub_type="kick_me")
class GroupDecreaseKickMeEvent(GroupDecreaseEvent):
    """
    机器人自己被移出事件
    """
    pass


@register_event("notice", notice_type="group_increase")
class GroupIncreaseEvent(NoticeEvent):
    """
    群成员增加事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.operator_id: int = int(self["operator_id"])
        self.sub_type: str = self["sub_type"]


@register_event("notice", notice_type="group_increase", sub_type="approve")
class GroupIncreaseApproveEvent(GroupIncreaseEvent):
    """
    群成员同意入群事件
    """
    pass


@register_event("notice", notice_type="group_increase", sub_type="invite")
class GroupIncreaseInviteEvent(GroupIncreaseEvent):
    """
    群成员被邀请入群事件
    """
    pass


@register_event("notice", notice_type="group_ban")
class GroupBanEvent(NoticeEvent):
    """
    群禁言事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.operator_id: int = int(self["operator_id"])
        self.sub_type: str = self["sub_type"]
        self.duration: int = int(self["duration"])


@register_event("notice", notice_type="group_ban", sub_type="ban")
class GroupBanSetEvent(GroupBanEvent):
    """
    群禁言被设置事件
    """
    pass


@register_event("notice", notice_type="group_ban", sub_type="lift_ban")
class GroupBanLiftEvent(GroupBanEvent):
    """
    群禁言被解除事件
    """
    pass


@register_event("notice", notice_type="friend_add")
class FriendAddEvent(NoticeEvent):
    """
    好友添加事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.user_id: int = int(self["user_id"])


@register_event("notice", notice_type="group_recall")
class GroupRecallEvent(NoticeEvent):
    """
    群消息撤回事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.operator_id: int = int(self["operator_id"])
        self.message_id: int = int(self["message_id"])


@register_event("notice", notice_type="friend_recall")
class FriendRecallEvent(NoticeEvent):
    """
    好友消息撤回事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.user_id: int = int(self["user_id"])
        self.message_id: int = int(self["message_id"])


@register_event("notice", notice_type="notify", sub_type="poke")
class GroupPokeEvent(NoticeEvent):
    """
    群戳一戳事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.target_id: int = int(self["target_id"])


@register_event("notice", notice_type="notify", sub_type="lucky_king")
class GroupLuckyKingEvent(NoticeEvent):
    """
    群红包运气王事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.target_id: int = int(self["target_id"])


@register_event("notice", notice_type="notify", sub_type="honor")
class GroupHonorEvent(NoticeEvent):
    """
    群荣誉变更事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.honor_type: str = self["honor_type"]


@register_event("notice", notice_type="notify", sub_type="honor", honor_type="talkative")
class GroupTalkativeHonorEvent(GroupHonorEvent):
    """
    群龙王变更事件
    """
    pass


@register_event("notice", notice_type="notify", sub_type="honor", honor_type="performer")
class GroupPerformerHonorEvent(GroupHonorEvent):
    """
    群群聊之火变更事件
    """
    pass


@register_event("notice", notice_type="notify", sub_type="honor", honor_type="emotion")
class GroupEmotionHonorEvent(GroupHonorEvent):
    """
    群表快乐源泉变更事件
    """
    pass


@register_event("request")
class RequestEvent(Event):
    """
    请求事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.request_type: str = self["request_type"]
        self.comment: str = self["comment"]
        self.flag: str = self["flag"]


@register_event("request", request_type="friend")
class FriendRequestEvent(RequestEvent):
    """
    加好友请求事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.user_id: int = int(self["user_id"])


@register_event("request", request_type="group")
class GroupRequestEvent(RequestEvent):
    """
    加群请求事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.sub_type: str = self["sub_type"]
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])


@register_event("request", request_type="group", sub_type="add")
class GroupAddRequestEvent(GroupRequestEvent):
    """
    加群请求事件 - 添加
    """
    pass


@register_event("request", request_type="group", sub_type="invite")
class GroupInviteRequestEvent(GroupRequestEvent):
    """
    加群请求事件 - 邀请
    """
    pass


@register_event("meta_event")
class MetaEvent(Event):
    """
    元事件
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.meta_event_type: str = self["meta_event_type"]


@register_event("meta_event", meta_event_type="lifecycle")
class LifecycleMetaEvent(MetaEvent):
    """
    元事件 - 生命周期
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.sub_type: str = self["sub_type"]


@register_event("meta_event", meta_event_type="lifecycle", sub_type="enable")
class EnableMetaEvent(LifecycleMetaEvent):
    """
    元事件 - 生命周期 - OneBot 启用
    """
    pass


@register_event("meta_event", meta_event_type="lifecycle", sub_type="disable")
class DisableMetaEvent(LifecycleMetaEvent):
    """
    元事件 - 生命周期 - OneBot 禁用
    """
    pass


@register_event("meta_event", meta_event_type="lifecycle", sub_type="connect")
class ConnectMetaEvent(LifecycleMetaEvent):
    """
    元事件 - 生命周期 - OneBot 连接成功
    """
    pass


@register_event("meta_event", meta_event_type="heartbeat")
class HeartbeatMetaEvent(MetaEvent):
    """
    元事件 - 心跳
    """
    def __init__(self, event_data):
        super().__init__(event_data)
        self.status: dict = self["status"]
        self.interval: int = int(self["interval"])


@EventManager.event_listener(ListenerServer.EscalationEvent)
def on_escalation(event_data):
    """
    事件分发器
    Args:
        event_data: 事件数据
    Returns:
        None
    """
    event_data = event_data.event_data
    event = Event(event_data)
    event.call()
    for event in events:
        if (
                event_data["post_type"] == event['post_type'] and
                all(k in event_data and event_data[k] == v for k, v in event['rules'].items())
        ):
            event = event['cls'](event_data)
            event.call()
