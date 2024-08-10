# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

"""
OnebotAPI
可以方便的调用Onebot的API
"""
import Lib.Configs as Configs
import Lib.EventManager as EventManager
import Lib.Logger as Logger
import requests
import threading
import traceback
import urllib.parse

logger = Logger.logger
cconfig = Configs.GlobalConfig()


class OnebotAPI:
    def __init__(self, host: str = cconfig.api_host, port: int = cconfig.api_port, original: bool = False):
        """
        :param host: 调用的ip
        :param port: 调用的端口
        :param original: 是否返回全部json（默认只返回data内）
        """
        # if url != "":
        #     url_list = urllib.parse.urlparse(url)
        #     host = url_list.scheme + "//" + url_list.netloc
        #     port = url_list.port
        #     node = url_list.path
        # else:
        #     node = ""
        self.host = host
        self.port = port
        self.node = ""
        self.data = None
        self.original = original

    def __str__(self):
        if not (self.host.startswith("http://") or self.host.startswith("https://")):
            self.host = "http://" + self.host
        # 拼接url
        self.url = urllib.parse.urljoin(self.host + ":" + str(self.port), self.node)
        return self.url

    def set_node(self, node: str, data: dict = None):
        if data is None:
            data = {}
        self.node = node
        self.data = data
        return self

    def set_ip(self, host: str, port: int):
        self.host = host
        self.port = port

    def set_data(self, data: dict):
        self.data = data
        return self

    def get(self, node: str = "", data: dict = None):
        if node != "":
            self.node = node
        if data is not None:
            self.data = data

        self.node = node
        self.data = data

        if self.node == "":
            # raise ValueError('The node cannot be empty.')
            self.node = "/"

        if self.host == "":
            raise ValueError('The host cannot be empty.')

        if self.port == -1:
            raise ValueError('The port cannot be empty.')

        # 广播call_api事件
        threading.Thread(target=EventManager.Event, args=(("call_api", self.node), self.data)).start()
        logger.debug(f"调用 API: {self.node} data: {self.data} by: {traceback.extract_stack()[-2].filename}")
        # 发起get请求
        try:
            response = requests.get(str(self), params=self.data)
            # 获取返回值
            result = response.json()['data']
            # 如果original为真，则返回原值和response
            if self.original:
                return result, response
            else:
                return result
        except Exception as e:
            # 返回异常信息
            return e

    def send_private_msg(self, user_id: int, message: str):
        """
        发送私聊消息
        :param user_id: 用户id
        :param message: 消息内容
        :return:
        """
        data = {
            "user_id": user_id,
            "message": message
        }
        return self.get("/send_private_msg", data)

    def send_group_msg(self, group_id: int, message: str):
        """
        发送群消息
        :param group_id: 群号
        :param message: 消息内容
        :return:
        """
        data = {
            "group_id": group_id,
            "message": message
        }
        return self.get("/send_group_msg", data)

    def send_msg(self, user_id: int = -1, group_id: int = -1, message: str = ""):
        """
        发送消息
        :param user_id: 用户id
        :param group_id: 群号
        :param message: 消息内容
        :return:
        """
        if user_id != -1 and group_id != -1:
            raise ValueError('user_id and group_id cannot be both not -1.')
        if user_id == -1 and group_id == -1:
            raise ValueError('user_id and group_id cannot be both -1.')
        if user_id != -1:
            return self.send_private_msg(user_id, message)
        elif group_id != -1:
            return self.send_group_msg(group_id, message)
        else:
            raise ValueError('user_id and group_id cannot be both -1.')

    def delete_msg(self, message_id: int):
        """
        删除消息
        :param message_id: 消息id
        :return:
        """
        data = {
            "message_id": message_id
        }
        return self.get("/delete_msg", data)

    def get_msg(self, message_id: int):
        """
        获取消息
        :param message_id: 消息id
        :return:
        """
        data = {
            "message_id": message_id
        }
        return self.get("/get_msg", data)

    def get_forward_msg(self, message_id: int):
        """
        获取合并转发消息
        :param message_id: 消息id
        :return:
        """
        data = {
            "message_id": message_id
        }
        return self.get("/get_forward_msg", data)

    def send_like(self, user_id: int, times: int = 1):
        """
        发送点赞
        :param user_id: 用户id
        :param times: 点赞次数
        :return:
        """
        data = {
            "user_id": user_id,
            "times": times
        }
        return self.get("/send_like", data)

    def set_group_kick(self, group_id: int, user_id: int, reject_add_request: bool = False):
        """
        群组踢人
        :param group_id: 群号
        :param user_id: 用户id
        :param reject_add_request: 拒绝加群请求
        :return:
        """
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "reject_add_request": reject_add_request
        }
        return self.get("/set_group_kick", data)

    def set_group_ban(self, group_id: int, user_id: int, duration: int = 30):
        """
        群组单人禁言
        :param group_id: 群号
        :param user_id: 用户id
        :param duration: 禁言时长，单位秒，无法取消禁言
        :return:
        """
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "duration": duration
        }
        return self.get("/set_group_ban", data)

    def set_group_anonymous_ban(self, group_id: int, anonymous: dict, duration: int = 600):
        """
        群组匿名用户禁言
        :param group_id: 群号
        :param anonymous: 匿名用户对象
        :param duration: 禁言时长，单位秒，无法取消禁言
        :return:
        """
        data = {
            "group_id": group_id,
            "anonymous": anonymous,
            "duration": duration
        }
        return self.get("/set_group_anonymous_ban", data)

    def set_group_whole_ban(self, group_id: int, enable: bool = True):
        """
        群组全员禁言
        :param group_id: 群号
        :param enable: 是否禁言
        :return:
        """
        data = {
            "group_id": group_id,
            "enable": enable
        }
        return self.get("/set_group_whole_ban", data)

    def set_group_admin(self, group_id: int, user_id: int, enable: bool = True):
        """
        群组设置管理员
        :param group_id: 群号
        :param user_id: 用户id
        :param enable: 是否设置管理员
        :return:
        """
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "enable": enable
        }
        return self.get("/set_group_admin", data)

    def set_group_card(self, group_id: int, user_id: int, card: str = ""):
        """
        设置群名片（群备注）
        :param group_id: 群号
        :param user_id: 用户id
        :param card: 群名片内容
        :return:
        """
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "card": card
        }
        return self.get("/set_group_card", data)

    def set_group_name(self, group_id: int, group_name: str):
        """
        设置群名
        :param group_id: 群号
        :param group_name: 群名
        :return:
        """
        data = {
            "group_id": group_id,
            "group_name": group_name
        }
        return self.get("/set_group_name", data)

    def set_group_leave(self, group_id: int, is_dismiss: bool = False):
        """
        :param group_id: 群号
        :param is_dismiss: 是否解散，如果登录号是群主，则仅在此项为True时能够解散
        :return:
        """
        data = {
            "group_id": group_id,
            "is_dismiss": is_dismiss
        }
        return self.get("/set_group_leave", data)

    def set_group_special_title(self, group_id: int, user_id: int, special_title: str = "", duration: int = -1):
        """
        设置群组专属头衔
        :param group_id: 群号
        :param user_id: 要设置的QQ号
        :param special_title: 专属头衔，不填或空字符串表示删除专属头衔
        :param duration: 专属头衔有效期，-1表示永久，其他值表示在此时间之前专属头衔会消失
        :return:
        """
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "special_title": special_title,
        }
        if duration != -1:
            data["duration"] = duration

        return self.get("/set_group_special_title", data)

    def set_friend_add_request(self, flag: str, approve: bool = True, remark: str = ""):
        """
        设置好友添加请求
        :param flag: 请求flag
        :param approve: 是否同意请求
        :param remark: 添加后的好友备注
        :return:
        """
        data = {
            "flag": flag,
            "approve": approve,
            "remark": remark
        }
        return self.get("/set_friend_add_request", data)

    def set_group_add_request(self, flag: str, sub_type: str = "add", approve: bool = True, reason: str = ""):
        """
        设置群添加请求
        :param flag: 请求flag
        :param sub_type: 添加请求类型，请参考api文档
        :param approve: 是否同意请求
        :param reason: 拒绝理由
        :return:
        """
        data = {
            "flag": flag,
            "sub_type": sub_type,
            "approve": approve,
            "reason": reason
        }
        return self.get("/set_group_add_request", data)

    def get_login_info(self):
        """
        获取登录号信息
        :return:
        """
        return self.get("/get_login_info")

    def get_stranger_info(self, user_id: int, no_cache: bool = False):
        """
        获取陌生人信息
        :param user_id: 对方QQ号
        :param no_cache: 是否不使用缓存（使用缓存可能更新不及时，但响应更快）
        :return:
        """
        data = {
            "user_id": user_id,
            "no_cache": no_cache
        }
        return self.get("/get_stranger_info", data)

    def get_friend_list(self):
        """
        获取好友列表
        :return:
        """
        return self.get("/get_friend_list")

    def get_group_info(self, group_id: int, no_cache: bool = False):
        """
        获取群信息
        :param group_id: 群号
        :param no_cache: 是否不使用缓存（使用缓存可能更新不及时，但响应更快）
        :return:
        """
        data = {
            "group_id": group_id,
            "no_cache": no_cache
        }
        return self.get("/get_group_info", data)

    def get_group_list(self):
        """
        获取群列表
        :return:
        """
        return self.get("/get_group_list")

    def get_group_member_info(self, group_id: int, user_id: int, no_cache: bool = False):
        """
        获取群成员信息
        :param group_id: 群号
        :param user_id: QQ号
        :param no_cache: 是否不使用缓存（使用缓存可能更新不及时，但响应更快）
        :return:
        """
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "no_cache": no_cache
        }
        return self.get("/get_group_member_info", data)

    def get_group_member_list(self, group_id: int, no_cache: bool = False):
        """
        获取群成员列表
        :param group_id: 群号
        :param no_cache: 是否不使用缓存（使用缓存可能更新不及时，但响应更快）
        :return:
        """
        data = {
            "group_id": group_id,
            "no_cache": no_cache
        }
        return self.get("/get_group_member_list", data)

    def get_group_honor_info(self, group_id: int, type_: str = "all"):
        """
        获取群荣誉信息
        :param group_id: 群号
        :param type_: 要获取的群荣誉类型，可传入 talkative performer legend strong_newbie emotion 以分别获取单个类型的群荣誉数据，或传入 all 获取所有数据
        :return:
        """
        data = {
            "group_id": group_id,
            "type": type_
        }
        return self.get("/get_group_honor_info", data)

    def get_cookies(self):
        """
        获取Cookies
        :return:
        """
        return self.get("/get_cookies")

    def get_csrf_token(self):
        """
        获取CSRF Token
        :return:
        """
        return self.get("/get_csrf_token")

    def get_credentials(self):
        """
        获取Credentials
        :return:
        """
        return self.get("/get_credentials")

    def get_record(self, file: str, out_format: str = "mp3", out_file: str = ""):
        """
        获取语音
        :param file: 文件ID
        :param out_format: 输出格式，mp3或amr，默认mp3
        :param out_file: 输出文件名，默认使用文件ID
        :return:
        """
        data = {
            "file": file,
            "out_format": out_format,
            "out_file": out_file
        }
        return self.get("/get_record", data)

    def get_image(self, file: str):
        """
        获取图片
        :param file: 文件ID
        :return:
        """
        data = {
            "file": file
        }
        return self.get("/get_image", data)

    def can_send_image(self):
        """
        检查是否可以发送图片
        :return:
        """
        return self.get("/can_send_image")

    def can_send_record(self):
        """
        检查是否可以发送语音
        :return:
        """
        return self.get("/can_send_record")

    def get_status(self):
        """
        获取运行状态
        :return:
        """
        return self.get("/get_status")

    def get_version_info(self):
        """
        获取版本信息
        :return:
        """
        return self.get("/get_version_info")

    def set_restart(self):
        """
        重启OneBot
        :return:
        """
        return self.get("/set_restart")

    def clean_cache(self):
        """
        清理缓存
        :return:
        """
        return self.get("/clean_cache")
