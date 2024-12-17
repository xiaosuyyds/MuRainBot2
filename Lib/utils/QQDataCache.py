import dataclasses
import time
from collections import OrderedDict

from ..core import OnebotAPI, ConfigManager
from . import Logger

NotFetched = type("NotFetched", (), {"__getattr__": lambda _, __: NotFetched,
                                     "__repr__": lambda _: "NotFetched",
                                     "__bool__": lambda _: False})
api = OnebotAPI.api
logger = Logger.get_logger()

expire_time = ConfigManager.GlobalConfig().qq_data_cache.expire_time


class QQDataItem:
    def __init__(self):
        self._data = NotFetched  # 数据
        self.last_update = time.time()  # 最后刷新时间

    def refresh_cache(self):
        self.last_update = time.time()

    def __getattr__(self, item):
        pass


class UserData(QQDataItem):
    def __init__(
            self,
            user_id: int,
            nickname: str = NotFetched,
            sex: str = NotFetched,
            age: int = NotFetched,
            is_friend: bool = NotFetched,
            remark: str | None = NotFetched  # 此值仅在是好友的时候会存在
    ):
        super().__init__()
        self._user_id = user_id
        self._data = {
            "user_id": user_id,
            "nickname": nickname,
            "sex": sex,
            "age": age,
            "is_friend": is_friend,
            "remark": remark
        }

    def refresh_cache(self):
        try:
            data = api.get_stranger_info(self._user_id)
            for k in data:
                self._data[k] = data[k]
            self._data["is_friend"] = NotFetched
            self._data["remark"] = NotFetched
        except Exception as e:
            logger.warn(f"获取用户{self._user_id}缓存信息失败: {repr(e)}")
            return

    def __getattribute__(self, item):
        data = super().__getattribute__("_data")
        if item not in list(data.keys()) + ["_data", "data"]:
            return super().__getattribute__(item)
        if item == "_data" or item == "data":
            return data

        if item in ["remark", "is_friend"] and data.get(item, None) != NotFetched:
            try:
                res = api.get_friend_list()
                for friend in res:
                    if friend["user_id"] == self._user_id:
                        self._data["remark"] = friend["remark"]
                        self._data["is_friend"] = True
                        break
                else:
                    self._data["is_friend"] = False
                    self._data["remark"] = None
            except Exception as e:
                logger.warn(f"获取用户{self._user_id}是否为好友失败: {repr(e)}")
                return None

        if data.get(item, None) == NotFetched or time.time() - self.last_update > expire_time:
            self.refresh_cache()

        if data.get(item, None) == NotFetched:
            return None

        return data.get(item, None)

    def get_nickname(self) -> str:
        return self.remark or self.nickname

    @property
    def data(self):
        return self._data

    @property
    def user_id(self):
        return self._user_id

    @property
    def nickname(self) -> str:
        return

    @property
    def sex(self) -> str:
        return

    @property
    def age(self) -> int:
        return

    @property
    def is_friend(self) -> bool:
        return

    @property
    def remark(self) -> str:
        return

    def __repr__(self):
        return f"UserData(user_id={self._user_id})"


class GroupMemberData(QQDataItem):
    def __init__(
            self,
            group_id: int,
            user_id: int,
            nickname: str = NotFetched,
            card: str = NotFetched,
            sex: str = NotFetched,
            age: int = NotFetched,
            area: str = NotFetched,
            join_time: int = NotFetched,
            last_sent_time: int = NotFetched,
            level: str = NotFetched,
            role: str = NotFetched,
            unfriendly: bool = NotFetched,
            title: str = NotFetched,
            title_expire_time: int = NotFetched,
            card_changeable: bool = NotFetched,
    ):
        super().__init__()
        self._group_id = group_id
        self._user_id = user_id
        self._data = {
            "group_id": group_id,
            "user_id": user_id,
            "nickname": nickname,
            "card": card,
            "sex": sex,
            "age": age,
            "area": area,
            "join_time": join_time,
            "last_sent_time": last_sent_time,
            "level": level,
            "role": role,
            "unfriendly": unfriendly,
            "title": title,
            "title_expire_time": title_expire_time,
            "card_changeable": card_changeable,
        }

    def refresh_cache(self):
        try:
            data = api.get_group_member_info(self._group_id, self._user_id, no_cache=True)
            for k in data:
                self._data[k] = data[k]
        except Exception as e:
            logger.warn(f"获取群{self._group_id}中成员{self._user_id}缓存信息失败: {repr(e)}")
            user_data = qq_data_cache.get_user_info(self._user_id)
            self._data["nickname"] = user_data.nickname if user_data.nickname else NotFetched
            self._data["sex"] = user_data.sex if user_data.sex else NotFetched
            self._data["age"] = user_data.age if user_data.age else NotFetched
        super().refresh_cache()

    def __getattribute__(self, item):
        data = super().__getattribute__("_data")
        if item not in list(data.keys()) + ["_data", "data"]:
            return super().__getattribute__(item)

        if item == "_data" or item == "data":
            return data

        if data.get(item, None) == NotFetched or time.time() - self.last_update > expire_time:
            self.refresh_cache()

        if data.get(item, None) == NotFetched:
            return None

        return data.get(item, None)

    @property
    def data(self):
        return self._data

    @property
    def group_id(self):
        return self._group_id

    @property
    def user_id(self):
        return self._user_id

    @property
    def nickname(self) -> str:
        return

    @property
    def card(self) -> str:
        return

    @property
    def sex(self) -> str:
        return

    @property
    def age(self) -> int:
        return

    @property
    def area(self) -> str:
        return

    @property
    def join_time(self) -> int:
        return

    @property
    def last_sent_time(self) -> int:
        return

    @property
    def level(self) -> str:
        return

    @property
    def role(self) -> str:
        return

    @property
    def unfriendly(self) -> bool:
        return

    @property
    def title(self) -> str:
        return

    @property
    def title_expire_time(self) -> int:
        return

    @property
    def card_changeable(self) -> bool:
        return

    def __str__(self):
        return f"GroupMemberData(group_id={self.group_id}, user_id={self.user_id})"

    def get_nickname(self):
        return self.card or self.nickname


class GroupData(QQDataItem):
    def __init__(
            self,
            group_id: int,
            group_name: str = NotFetched,
            member_count: int = NotFetched,
            max_member_count: int = NotFetched
    ):
        super().__init__()
        self._group_id = group_id
        self._data = {
            "group_id": group_id,
            "group_name": group_name,
            "member_count": member_count,
            "max_member_count": max_member_count,
            "group_member_list": NotFetched
        }

    def refresh_cache(self):
        try:
            data = api.get_group_info(group_id=self._group_id, no_cache=True)
            for k in data:
                self._data[k] = data[k]
            self._data["group_member_list"] = NotFetched
        except Exception as e:
            logger.warn(f"获取群{self._group_id}缓存信息失败: {repr(e)}")
            return
        super().refresh_cache()

    def __getattribute__(self, item):
        data = super().__getattribute__("_data")
        if item not in list(data.keys()) + ["_data", "data"]:
            return super().__getattribute__(item)

        if item == "_data" or item == "data":
            return data

        if item == "group_member_list" and data.get(item, None) == NotFetched:
            try:
                res = api.get_group_member_list(self._group_id)
                member_list = [GroupMemberData(**{k: (v if v is not None else NotFetched)
                                                  for k, v in member.items()})
                               for member in res]
                self._data[item] = member_list
            except Exception as e:
                logger.warn(f"获取群{self._group_id}成员列表信息失败: {repr(e)}")
                return

        if data.get(item, None) == NotFetched or time.time() - self.last_update > expire_time:
            self.refresh_cache()

        if data.get(item, None) == NotFetched:
            return None

        return data.get(item, None)

    def __str__(self):
        return f"GroupData(group_id={self._group_id})"

    @property
    def data(self):
        return self._data

    @property
    def group_id(self):
        return self._group_id

    @property
    def group_name(self) -> str:
        return

    @property
    def member_count(self) -> int:
        return

    @property
    def max_member_count(self) -> int:
        return

    @property
    def group_member_list(self) -> list[GroupMemberData]:
        return


class QQDataCache:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.group_info = {}
        self.group_member_info = {}
        self.user_info = {}
        self.max_cache_size = ConfigManager.GlobalConfig().qq_data_cache.max_cache_size
        self.expire_time = ConfigManager.GlobalConfig().qq_data_cache.expire_time

    def get_user_info(self, user_id: int, *args, **kwargs) -> UserData:
        if user_id not in self.user_info:
            data = UserData(user_id, *args, **kwargs)
            self.user_info[user_id] = data

        data = self.user_info[user_id]
        return data

    def get_group_info(self, group_id: int, *args, **kwargs) -> GroupData:
        if group_id not in self.group_info:
            data = GroupData(group_id, *args, **kwargs)
            self.group_info[group_id] = data

        data = self.group_info[group_id]
        return data

    def get_group_member_info(self, group_id: int, user_id: int, *args, **kwargs) -> GroupMemberData:
        if group_id not in self.group_member_info:
            self.group_member_info[group_id] = {}

        if user_id not in self.group_member_info[group_id]:
            data = GroupMemberData(group_id, user_id, *args, **kwargs)
            self.group_member_info[group_id][user_id] = data

        data = self.group_member_info[group_id][user_id]
        return data


qq_data_cache = QQDataCache()
