import dataclasses
from typing import TypedDict, NotRequired, Any, Literal

from ..core import EventManager, ListenerServer
from . import QQRichText


class Event(EventManager.Event):
    def __init__(self, event_data):
        self.event_data: dict = event_data
        self.time: int = self["time"]
        self.self_id: int = self["self_id"]
        self.post_type: str = self["post_type"]

    def __getitem__(self, item):
        return self.event_data.get(item)

    def __contains__(self, other):
        return other in self.event_data

    def __repr__(self):
        return str(self.event_data)


class EventData(TypedDict):
    cls: Event
    post_type: str
    rules: dict


events: list[EventData] = []


def register_event(post_type: str, **other_rules):
    def decorator(cls):
        data: EventData = {
            "cls": cls,
            "post_type": post_type,
            "rules": other_rules
        }
        events.append(data)
        return cls

    return decorator


class SenderDict(TypedDict, total=False):
    user_id: NotRequired[int]
    nickname: NotRequired[str]
    sex: NotRequired[Literal["male", "female", "unknown"]]
    age: NotRequired[int]


class PrivateDict(TypedDict, total=False):
    user_id: NotRequired[int]
    nickname: NotRequired[str]
    sex: NotRequired[Literal["male", "female", "unknown"]]
    age: NotRequired[int]


class GroupSenderDict(TypedDict, total=False):
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
    def __init__(self, event_data):
        super().__init__(event_data)
        self.sender: PrivateDict = self["sender"]


@register_event("message", message_type="group")
class GroupMessageEvent(MessageEvent):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.sender: GroupSenderDict = self["sender"]


@register_event("notice")
class NoticeEvent(Event):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.notice_type: str = self["notice_type"]


class FileDict(TypedDict, total=False):
    id: str
    name: str
    size: int
    busid: int


@register_event("notice", notice_type="group_upload")
class GroupUploadEvent(NoticeEvent):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.file: FileDict = self["file"]


@register_event("notice", notice_type="group_admin")
class GroupAdminEvent(NoticeEvent):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.sub_type: str = self["sub_type"]


@register_event("notice", notice_type="group_admin", sub_type="set")
class GroupSetAdminEvent(GroupAdminEvent):
    pass


@register_event("notice", notice_type="group_admin", sub_type="unset")
class GroupUnsetAdminEvent(GroupAdminEvent):
    pass


@register_event("notice", notice_type="group_decrease")
class GroupDecreaseEvent(NoticeEvent):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.operator_id = int(self["operator_id"])
        self.sub_type: str = self["sub_type"]


@register_event("notice", notice_type="group_decrease", sub_type="leave")
class GroupDecreaseLeaveEvent(GroupDecreaseEvent):
    pass


@register_event("notice", notice_type="group_decrease", sub_type="kick")
class GroupDecreaseKickEvent(GroupDecreaseEvent):
    pass


@register_event("notice", notice_type="group_decrease", sub_type="kick_me")
class GroupDecreaseKickMeEvent(GroupDecreaseEvent):
    pass


@register_event("notice", notice_type="group_increase")
class GroupIncreaseEvent(NoticeEvent):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.operator_id: int = int(self["operator_id"])
        self.sub_type: str = self["sub_type"]


@register_event("notice", notice_type="group_increase", sub_type="approve")
class GroupIncreaseApproveEvent(GroupIncreaseEvent):
    pass


@register_event("notice", notice_type="group_increase", sub_type="invite")
class GroupIncreaseInviteEvent(GroupIncreaseEvent):
    pass


@register_event("notice", notice_type="group_ban")
class GroupBanEvent(NoticeEvent):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.operator_id: int = int(self["operator_id"])
        self.sub_type: str = self["sub_type"]
        self.duration: int = int(self["duration"])


@register_event("notice", notice_type="group_ban", sub_type="ban")
class GroupBanSetEvent(GroupBanEvent):
    pass


@register_event("notice", notice_type="group_ban", sub_type="lift_ban")
class GroupBanLiftEvent(GroupBanEvent):
    pass


@register_event("notice", notice_type="friend_add")
class FriendAddEvent(NoticeEvent):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.user_id: int = int(self["user_id"])


@register_event("notice", notice_type="group_recall")
class GroupRecallEvent(NoticeEvent):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.operator_id: int = int(self["operator_id"])
        self.message_id: int = int(self["message_id"])


@register_event("notice", notice_type="friend_recall")
class FriendRecallEvent(NoticeEvent):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.user_id: int = int(self["user_id"])
        self.message_id: int = int(self["message_id"])


@register_event("notice", notice_type="notify", sub_type="poke")
class GroupPokeEvent(NoticeEvent):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.target_id: int = int(self["target_id"])


@register_event("notice", notice_type="notify", sub_type="lucky_king")
class GroupLuckyKingEvent(NoticeEvent):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.target_id: int = int(self["target_id"])


@register_event("notice", notice_type="notify", sub_type="honor")
class GroupHonorEvent(NoticeEvent):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])
        self.honor_type: str = self["honor_type"]


@register_event("notice", notice_type="notify", sub_type="honor", honor_type="talkative")
class GroupTalkativeHonorEvent(GroupHonorEvent):
    pass


@register_event("notice", notice_type="notify", sub_type="honor", honor_type="performer")
class GroupPerformerHonorEvent(GroupHonorEvent):
    pass


@register_event("notice", notice_type="notify", sub_type="honor", honor_type="emotion")
class GroupEmotionHonorEvent(GroupHonorEvent):
    pass


@register_event("request")
class RequestEvent(Event):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.request_type: str = self["request_type"]
        self.comment: str = self["comment"]
        self.flag: str = self["flag"]


@register_event("request", request_type="friend")
class FriendRequestEvent(RequestEvent):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.user_id: int = int(self["user_id"])


@register_event("request", request_type="group")
class GroupRequestEvent(RequestEvent):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.sub_type: str = self["sub_type"]
        self.group_id: int = int(self["group_id"])
        self.user_id: int = int(self["user_id"])


@register_event("request", request_type="group", sub_type="add")
class GroupAddRequestEvent(GroupRequestEvent):
    pass


@register_event("request", request_type="group", sub_type="invite")
class GroupInviteRequestEvent(GroupRequestEvent):
    pass


@register_event("meta_event")
class MetaEvent(Event):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.meta_event_type: str = self["meta_event_type"]


@register_event("meta_event", meta_event_type="lifecycle")
class LifecycleMetaEvent(MetaEvent):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.sub_type: str = self["sub_type"]


@register_event("meta_event", meta_event_type="lifecycle", sub_type="enable")
class EnableMetaEvent(LifecycleMetaEvent):
    pass


@register_event("meta_event", meta_event_type="lifecycle", sub_type="disable")
class DisableMetaEvent(LifecycleMetaEvent):
    pass


@register_event("meta_event", meta_event_type="lifecycle", sub_type="connect")
class ConnectMetaEvent(LifecycleMetaEvent):
    pass


@register_event("meta_event", meta_event_type="heartbeat")
class HeartbeatMetaEvent(MetaEvent):
    def __init__(self, event_data):
        super().__init__(event_data)
        self.time: int = int(self["time"])
        self.self_id: int = int(self["self_id"])
        self.status: dict = self["status"]
        self.interval: int = int(self["interval"])


@EventManager.event_listener(ListenerServer.EscalationEvent)
def on_escalation(event_data):
    event_data = event_data.event_data
    for event in events:
        if (
                event_data["post_type"] == event['post_type'] and
                all(k in event_data and event_data[k] == v for k, v in event['rules'].items())
        ):
            event = event['cls'](event_data)
            event.call()
