from collections.abc import Callable

from . import Logger, QQDataCache
from ..core import EventManager, ListenerServer

qq_data = QQDataCache.qq_data_cache
logger = Logger.get_logger()


class Rule:
    def __init__(self, item: str | Callable[[ListenerServer.EscalationEvent], bool], value):
        self.item = item
        self.value = value
        if isinstance(self.item, str):
            self.item_type = "key"
        elif isinstance(self.item, Callable):
            self.item_type = "code"
        else:
            raise TypeError("Rule item must be str or callable")

    def is_valid(self, event: ListenerServer.EscalationEvent) -> bool:
        if self.item_type == "key":
            return self.item in event.event_data and (self.value is None or event.event_data[self.item] == self.value)
        elif self.item_type == "code":
            return self.item(event)

    def __repr__(self):
        return f"Rule(item={self.item}, value={self.value})"


class Node:
    def __init__(self, rules: list[Rule], value):
        self.rules: list[Rule] = rules
        self.value: str | Callable | list = value
        if isinstance(value, str) or isinstance(value, Callable):
            self.value_type = "code"
            if isinstance(value, str):
                self.value = lambda _: eval(value)
        elif isinstance(value, Node):
            self.value_type = "nodes"
            self.value = [value]
        elif isinstance(value, list):
            for item in value:
                if not isinstance(item, Node):
                    raise TypeError("Node value must be Node or list of Node")
            self.value_type = "nodes"
        else:
            raise TypeError("Node value must be Node or list of Node or callable or str")

    def is_valid(self, event: ListenerServer.EscalationEvent) -> bool:
        return all(rule.is_valid(event) for rule in self.rules)

    def __repr__(self):
        return f"Node(rules={self.rules}, value={self.value})"


root_node = Node(
    [Rule(lambda x: True, None)],
    [
        # 消息事件
        Node(
            [Rule("post_type", "message")],
            [
                #  群聊消息
                Node(
                    [
                        Rule("message_type", "group")
                    ],
                    [
                        # 普通消息
                        Node(
                            [
                                Rule("sub_type", "normal")
                            ],
                            lambda event_data:
                            logger.info(
                                f"收到来自群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']})"
                                f" 内成员 "
                                f"{qq_data.get_group_member_info(
                                    event_data['group_id'], event_data['user_id'],
                                    **{k: v for k, v in event_data.get('sender', {}).items()
                                       if k not in ['group_id', 'user_id']}).get_nickname()}"
                                f"({event_data['user_id']}) "
                                f"的消息: "
                                f"{event_data['message']}"
                                f"({event_data['message_id']})"
                            )
                        ),
                        # 匿名消息
                        Node(
                            [
                                Rule("sub_type", "anonymous")
                            ],
                            lambda event_data:
                            logger.info(
                                f"收到来自群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']})"
                                f" 内 "
                                f"{qq_data.get_user_info(event_data['anonymous']).get('name')}"
                                f"({event_data['anonymous']['id']}; flag: {event_data['anonymous']['flag']}) "
                                f"的匿名消息: "
                                f"{event_data['message']}"
                                f"({event_data['message_id']})"
                            )
                        ),
                        # 系统消息
                        Node(
                            [
                                Rule("sub_type", "notice")
                            ],
                            lambda event_data:
                            logger.info(
                                f"收到来自群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']}) "
                                f"内的系统消息: "
                                f"{event_data['message']}"
                                f"({event_data['message_id']})"
                            )
                        )
                    ]
                ),
                Node(
                    [
                        Rule("message_type", "private")
                    ],
                    [
                        # 好友消息
                        Node(
                            [
                                Rule("sub_type", "friend")
                            ],
                            lambda event_data:
                            logger.info(
                                f"收到来自好友 "
                                f"{qq_data.get_user_info(
                                    event_data['user_id'],
                                    **{k: v for k, v in event_data.get('sender', {}).items()
                                       if k not in ['user_id']}
                                ).nickname}"
                                f"({event_data['user_id']}) "
                                f"的消息: "
                                f"{event_data['message']}"
                                f"({event_data['message_id']})"
                            )
                        ),
                        # 群临时会话消息
                        Node(
                            [
                                Rule("sub_type", "group")
                            ],
                            lambda event_data:
                            logger.info(
                                f"收到来自群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']})"
                                f" 内成员 "
                                f"{qq_data.get_group_member_info(
                                    event_data['group_id'], event_data['user_id'],
                                    **{k: v for k, v in event_data.get('sender', {}).items()
                                       if k not in ['group_id', 'user_id']}).get_nickname()}"
                                f"({event_data['user_id']}) "
                                f"的群临时会话消息: "
                                f"{event_data['message']}"
                                f"({event_data['message_id']})"
                            )
                        ),
                        # 其他
                        Node(
                            [
                                Rule("sub_type", "other")
                            ],
                            lambda event_data:
                            logger.info(
                                f"收到来自 "
                                f"{qq_data.get_user_info(
                                    event_data['user_id'],
                                    **{k: v for k, v in event_data.get('sender', {}).items()
                                       if k not in ['user_id']}
                                ).nickname}"
                                f"({event_data['user_id']}) "
                                f"的消息: "
                                f"{event_data['message']}"
                                f"({event_data['message_id']})"
                            )
                        )
                    ]
                )
            ]
        )
    ]
)


def run_node(node: Node, event: ListenerServer.EscalationEvent):
    if node.is_valid(event):
        if node.value_type == "code":
            node.value(event.event_data)

        elif node.value_type == "nodes":
            for item in node.value:
                run_node(item, event)


@EventManager.event_listener(ListenerServer.EscalationEvent)
def on_escalation(event):
    run_node(root_node, event)
