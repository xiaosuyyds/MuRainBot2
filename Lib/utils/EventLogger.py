from collections.abc import Callable

from . import Logger, QQDataCacher, QQRichText
from ..core import EventManager, ListenerServer

qq_data = QQDataCacher.qq_data_cache
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
    def __init__(self, rules: list[Rule], value: str | Callable | list):
        self.rules: list[Rule] = rules
        if isinstance(value, Node):
            self.value = value
        elif isinstance(value, list):
            for item in value:
                if not isinstance(item, Node):
                    raise TypeError("Node value must be Node or list of Node")
            self.value = value
            self.value_type = "nodes"
        elif isinstance(value, str) or isinstance(value, Callable):
            self.value_type = "code"
            if isinstance(value, str):
                self.value = lambda _: eval(value)
            else:
                self.value = value
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
                                f"{QQRichText.QQRichText(event_data['message']).
                                   render(group_id=event_data['group_id'])}"
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
                                f"{QQRichText.QQRichText(event_data['message']).
                                   render(group_id=event_data['group_id'])}"
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
                                f"{QQRichText.QQRichText(event_data['message']).
                                   render(group_id=event_data['group_id'])}"
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
                                    is_friend=True,
                                    **{k: v for k, v in event_data.get('sender', {}).items()
                                       if k not in ['user_id']}
                                ).nickname}"
                                f"({event_data['user_id']}) "
                                f"的消息: "
                                f"{QQRichText.QQRichText(event_data['message']).render()}"
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
                                f"{QQRichText.QQRichText(event_data['message']).render()}"
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
                                f"{QQRichText.QQRichText(event_data['message']).render()}"
                                f"({event_data['message_id']})"
                            )
                        )
                    ]
                )
            ]
        ),
        # 通知事件
        Node(
            [
                Rule("post_type", "notice")
            ],
            [
                # 群文件上传
                Node(
                    [
                        Rule("notice_type", "group_upload")
                    ],
                    lambda event_data:
                    logger.info(
                        f"群 "
                        f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                        f"({event_data['group_id']}) "
                        f"内成员 "
                        f"{qq_data.get_user_info(event_data['user_id']).get_nickname()} "
                        f"({event_data['user_id']}) "
                        f"上传了文件: "
                        f"{event_data['file']['name']}"
                        f"({event_data['file']['id']})"
                    )
                ),
                # 群管理员变动
                Node(
                    [
                        Rule("notice_type", "group_admin")
                    ],
                    [
                        # 设置管理员
                        Node(
                            [
                                Rule("sub_type", "set")
                            ],
                            lambda event_data:
                            logger.info(
                                f"群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']}) "
                                f"内 成员 "
                                f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                                f"({event_data['user_id']}) "
                                f"被设置为管理员"
                            )
                        ),
                        # 取消管理员
                        Node(
                            [
                                Rule("sub_type", "unset")
                            ],
                            lambda event_data:
                            logger.info(
                                f"群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']}) "
                                f"内 成员 "
                                f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                                f"({event_data['user_id']}) "
                                f"被取消管理员"
                            )
                        )
                    ]
                ),
                # 群成员减少
                Node(
                    [
                        Rule("notice_type", "group_decrease")
                    ],
                    [
                        Node(
                            [
                                Rule("sub_type", "leave")
                            ],
                            lambda event_data:
                            logger.info(
                                f"群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']}) "
                                f"内成员 "
                                f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                                f"({event_data['user_id']}) "
                                f"退出了群聊"
                            )
                        ),
                        Node(
                            [
                                Rule("sub_type", "kick")
                            ],
                            lambda event_data:
                            logger.info(
                                f"群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']}) "
                                f"内成员 "
                                f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                                f"({event_data['user_id']}) "
                                f"被管理员 "
                                f"{qq_data.get_user_info(event_data['operator_id']).get_nickname()}"
                                f"({event_data['operator_id']}) "
                                f"踢出了群聊"
                            )
                        ),
                        Node(
                            [
                                Rule("sub_type", "kick_me")
                            ],
                            lambda event_data:
                            logger.info(
                                f"群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']}) "
                                f"内 "
                                f"{qq_data.get_user_info(event_data['operator_id']).get_nickname()}"
                                f"({event_data['operator_id']}) "
                                f"将机器人踢出了群聊"
                            )
                        )
                    ]
                ),
                # 群成员增加
                Node(
                    [
                        Rule("notice_type", "group_increase")
                    ],
                    [
                        Node(
                            [
                                Rule("sub_type", "approve")
                            ],
                            lambda event_data:
                            logger.info(
                                f"群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']}) "
                                f"内成员 "
                                f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                                f"({event_data['user_id']}) "
                                f"被管理员 "
                                f"{qq_data.get_user_info(event_data['operator_id']).get_nickname()}"
                                f"({event_data['operator_id']}) "
                                f"批准入群"
                            ),
                        ),
                        Node(
                            [
                                Rule("sub_type", "invite")
                            ],
                            lambda event_data:
                            logger.info(
                                f"群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']}) "
                                f"内成员 "
                                f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                                f"({event_data['user_id']}) "
                                f"被 "
                                f"{qq_data.get_user_info(event_data['operator_id']).get_nickname()}"
                                f"({event_data['operator_id']}) "
                                f"邀请入群"
                            )
                        )
                    ]
                ),
                # 群禁言
                Node(
                    [
                        Rule("notice_type", "group_ban")
                    ],
                    [
                        Node(
                            [
                                Rule("sub_type", "ban")
                            ],
                            lambda event_data:
                            logger.info(
                                f"群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']}) "
                                f"内成员 "
                                f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                                f"({event_data['user_id']}) "
                                f"被管理员 "
                                f"{qq_data.get_user_info(event_data['operator_id']).get_nickname()}"
                                f"({event_data['operator_id']}) "
                                f"禁言了: "
                                f"{event_data['duration']}s"
                            )
                        ),
                        Node(
                            [
                                Rule("sub_type", "lift_ban")
                            ],
                            lambda event_data:
                            logger.info(
                                f"群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']}) "
                                f"内成员 "
                                f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                                f"({event_data['user_id']}) "
                                f"被管理员 "
                                f"{qq_data.get_user_info(event_data['operator_id']).get_nickname()}"
                                f"({event_data['operator_id']}) "
                                f"解除了禁言"
                            )
                        )
                    ]
                ),
                # 好友添加
                Node(
                    [
                        Rule("notice_type", "friend_add")
                    ],
                    lambda event_data:
                    logger.info(
                        f"好友 "
                        f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                        f"({event_data['user_id']}) "
                        f"添加了机器人的好友"
                    )
                ),
                # 群消息撤回
                Node(
                    [
                        Rule("notice_type", "group_recall")
                    ],
                    [
                        Node(
                            [
                                Rule(
                                    lambda event_data:
                                    event_data["user_id"] == event_data.event_data["operator_id"],
                                    None
                                )
                            ],
                            lambda event_data:
                            logger.info(
                                f"群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']}) "
                                f"内成员 "
                                f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                                f"({event_data['user_id']}) "
                                f"撤回了消息: "
                                f"{event_data['message_id']}"
                            )
                        ),
                        Node(
                            [
                                Rule(
                                    lambda event_data:
                                    event_data["user_id"] != event_data.event_data["operator_id"],
                                    None
                                )
                            ],
                            lambda event_data:
                            logger.info(
                                f"群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']}) "
                                f"内成员 "
                                f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                                f"({event_data['user_id']}) "
                                f"被管理员 "
                                f"{qq_data.get_user_info(event_data['operator_id']).get_nickname()}"
                                f"({event_data['operator_id']}) "
                                f"撤回了消息: "
                                f"{event_data['message_id']}"
                            )
                        )
                    ]
                ),
                # 好友消息撤回
                Node(
                    [
                        Rule("notice_type", "friend_recall")
                    ],
                    lambda event_data:
                    logger.info(
                        f"好友 "
                        f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                        f"({event_data['user_id']}) "
                        f"撤回了消息: "
                        f"{event_data['message_id']}"
                    )
                ),
                # 通知
                Node(
                    [
                        Rule("notice_type", "notify")
                    ],
                    [
                        # 群内戳一戳
                        Node(
                            [
                                Rule("sub_type", "poke")
                            ],
                            lambda event_data:
                            logger.info(
                                f"群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']}) "
                                f"内 "
                                f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                                f"({event_data['user_id']}) "
                                f"戳了戳 "
                                f"{qq_data.get_user_info(event_data['target_id']).get_nickname()}"
                                f"({event_data['target_id']})"
                            )
                        ),
                        # 红包运气王
                        Node(
                            [
                                Rule("sub_type", "lucky_king")
                            ],
                            lambda event_data:
                            logger.info(
                                f"群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']}) "
                                f"内 "
                                f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                                f"({event_data['user_id']}) "
                                f"成为了 "
                                f"{qq_data.get_user_info(event_data['target_id']).get_nickname()}"
                                f"({event_data['target_id']}) "
                                f"发送的红包的运气王"
                            )
                        ),
                        # 群成员荣誉变更
                        Node(
                            [
                                Rule("sub_type", "honor")
                            ],
                            lambda event_data:
                            logger.info(
                                f"群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']}) "
                                f"内 "
                                f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                                f"({event_data['user_id']}) "
                                f"获得了 " + {
                                    "talkative": "群聊之火",
                                    "performer": "群聊炽焰",
                                    "emotion": "快乐源泉"
                                }[event_data['honor_type']] +
                                " 的称号"
                            )
                        )
                    ]
                )
            ]
        ),
        # 请求事件
        Node(
            [
                Rule("post_type", "request")
            ],
            [
                # 添加好友请求
                Node(
                    [
                        Rule("request_type", "friend")
                    ],
                    lambda event_data:
                    logger.info(
                        f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                        f"({event_data['user_id']})"
                        f"请求添加机器人为好友\n"
                        f"验证信息: {event_data['comment']}\n"
                        f"flag: {event_data['flag']}"
                    )
                ),
                # 加群请求/邀请
                Node(
                    [
                        Rule("request_type", "group")
                    ],
                    [
                        # 加群请求
                        Node(
                            [
                                Rule("sub_type", "add")
                            ],
                            lambda event_data:
                            logger.info(
                                f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                                f"({event_data['user_id']})"
                                f"请求加入群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                                f"({event_data['group_id']})\n"
                                f"验证信息: {event_data['comment']}\n"
                                f"flag: {event_data['flag']}"
                            )
                        ),
                        # 加群邀请
                        Node(
                            [
                                Rule("sub_type", "invite")
                            ],
                            lambda event_data:
                            logger.info(
                                f"{qq_data.get_user_info(event_data['user_id']).get_nickname()}"
                                f"({event_data['user_id']})"
                                f"邀请机器人加入群 "
                                f"{qq_data.get_group_info(event_data['group_id']).group_name}"
                            )
                        )
                    ]
                )
            ]
        ),
        # 元事件
        Node(
            [
                Rule("post_type", "meta_event")
            ],
            [
                # 生命周期
                Node(
                    [
                        Rule("meta_event_type", "lifecycle")
                    ],
                    lambda event_data:
                    logger.info(
                        f"收到元事件: " + {
                            "enable": "OneBot 启用",
                            "disable": "OneBot 禁用",
                            "connect": "OneBot 连接成功"
                        }[event_data['sub_type']]
                    )
                ),
                # 心跳
                Node(
                    [
                        Rule("meta_event_type", "heartbeat")
                    ],
                    lambda event_data:
                    logger.debug(
                        f"收到心跳包"
                    )
                )
            ]
        )
    ]
)


def run_node(node: Node, event: ListenerServer.EscalationEvent):
    flag = False
    if node.is_valid(event):
        if node.value_type == "code":
            node.value(event.event_data)
            flag = True

        elif node.value_type == "nodes":
            for item in node.value:
                if run_node(item, event):
                    flag = True
    return flag


@EventManager.event_listener(ListenerServer.EscalationEvent)
def on_escalation(event):
    flag = run_node(root_node, event)
    if not flag:
        logger.warning(f"未匹配到任何事件处理器，未知的上报: {event.event_data}")
