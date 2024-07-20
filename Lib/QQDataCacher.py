import Lib.OnebotAPI as OnebotAPI
import Lib.Configs as Configs
import Lib.Logger as Logger
import Lib.MuRainLib as MuRainLib
import threading
import time

api = OnebotAPI.OnebotAPI()
config = Configs.GlobalConfig()
logger = Logger.logger

user_cache = MuRainLib.LimitedSizeDict(max_size=config.max_cache_size)
group_cache = MuRainLib.LimitedSizeDict(max_size=config.max_cache_size)
group_member_cache = MuRainLib.LimitedSizeDict(max_size=config.max_cache_size)


class UserData:
    def __init__(
            self,
            user_id: int,
            name: str | None = None,
            sex: str | None = None,
            age: int | None = None,
    ):
        self.user_id = user_id
        self.nickname = name
        self.sex = sex
        self.age = age

        if self.nickname or self.sex or self.age is None:
            self.refresh_cache()

        if user_id not in user_cache and config.qq_data_cache:
            user_cache[user_id] = self

    def refresh_cache(self):
        data = api.get_stranger_info(self.user_id, no_cache=True)
        if data is None and isinstance(data, dict):
            self.nickname = data.get("nickname")
            self.sex = data.get("sex")
            self.age = data.get("age")


class GroupMemberData:
    def __init__(
            self,
            user_id: int,
            group_id: int,
            name: str | None = None,
            card: str | None = None,
            sex: str | None = None,
            age: int | None = None,
            area: str | None = None,
            join_time: int | None = None,
            last_sent_time: int | None = None,
            level: int | None = None,
            role: str | None = None,
            title: str | None = None,
            title_expire_time: int | None = None,
            card_changeable: bool | None = None,
    ):
        self.user_id = user_id
        self.group_id = group_id

        self.nickname = name
        self.card = card
        self.sex = sex
        self.age = age
        self.area = area
        self.join_time = join_time
        self.last_sent_time = last_sent_time
        self.level = level
        self.role = role
        self.title = title
        self.title_expire_time = title_expire_time
        self.card_changeable = card_changeable
        if (self.nickname is None or self.card is None or self.sex is None or self.age is None
                or self.area is None or self.join_time is None
                or self.last_sent_time is None or self.level is None
                or self.role is None or self.title is None
                or self.title_expire_time is None or self.card_changeable is None):
            self.refresh_cache()

        if group_id not in group_member_cache and config.qq_data_cache:
            if user_id not in group_member_cache[group_id]:
                group_member_cache[group_id][user_id] = self

    def refresh_cache(self):
        data = api.get_group_member_info(self.group_id, self.user_id, no_cache=True)
        if data is not None and isinstance(data, dict):
            self.nickname = data.get("nickname")
            self.card = data.get("card")
            self.sex = data.get("sex")
            self.age = data.get("age")
            self.area = data.get("area")
            self.join_time = data.get("join_time")
            self.last_sent_time = data.get("last_sent_time")
            self.level = data.get("level")
            self.role = data.get("role")
            self.title = data.get("title")
            self.title_expire_time = data.get("title_expire_time")
            self.card_changeable = data.get("card_changeable")
        else:
            data = api.get_stranger_info(self.user_id)
            if data is not None:
                self.nickname = data.get("nickname")
                self.sex = data.get("sex")
                self.age = data.get("age")

    def get_group_name(self):
        if self.card != "" and self.card is not None:
            return self.card

        return self.nickname


class GroupData:
    def __init__(
            self,
            group_id,
            name: str | None = None,
            member_count: int | None = None,
            max_member_count: int | None = None,
    ):
        self.group_id = group_id

        self.group_name = name
        self.member_count = member_count
        self.max_member_count = max_member_count

        if self.group_name is None or self.member_count is None or self.max_member_count is None:
            data = api.get_group_info(self.group_id, no_cache=True)
            if data is not None:
                self.refresh_cache()

        data = api.get_group_member_list(self.group_id, no_cache=True)
        if data is not None and isinstance(data, dict):
            self.group_member_list = []
            for member in data:
                self.group_member_list.append(GroupMemberData(member.get("user_id"), group_id))
        else:
            self.group_member_list = None

        if group_id not in group_cache and self.group_member_list is not None:
            group_cache[group_id] = self

    def refresh_cache(self):
        data = api.get_group_info(self.group_id, no_cache=True)
        if data is not None and isinstance(data, dict):
            self.group_name = data.get("group_name")
            self.member_count = data.get("member_count")
            self.max_member_count = data.get("max_member_count")
            self.group_member_list = []
        data = api.get_group_member_list(self.group_id, no_cache=True)
        if data is not None and isinstance(data, dict):
            self.group_member_list = []
            for member in data:
                self.group_member_list.append(
                    GroupMemberData(
                        member.get("user_id"),
                        self.group_id,
                        name=member.get("nickname"),
                        card=member.get("card"),
                        sex=member.get("sex"),
                        age=member.get("age"),
                        area=member.get("area"),
                        join_time=member.get("join_time"),
                        last_sent_time=member.get("last_sent_time"),
                        level=member.get("level"),
                        role=member.get("role"),
                        title=member.get("title"),
                        title_expire_time=member.get("title_expire_time"),
                        card_changeable=member.get("card_changeable")
                    )
                )
        else:
            self.group_member_list = None


def get_user_data(user_id):
    if user_id in list(user_cache.keys()):
        return user_cache[user_id]

    return UserData(user_id)


def get_group_data(group_id):
    if group_id in list(group_cache.keys()):
        return group_cache[group_id]

    return GroupData(group_id)


def get_group_user_data(group_id, user_id):
    if group_id in group_member_cache and user_id in group_member_cache[group_id]:
        return group_member_cache[group_id][user_id]

    if group_id in list(group_cache.keys()) and group_cache[group_id].group_member_list is not None:
        for member in group_cache[group_id].group_member_list:
            if member.user_id == user_id:
                return member

    return GroupMemberData(user_id, group_id)


def refresh_all_cache():
    for group_id in list(group_cache.keys()):
        group_cache[group_id].refresh_cache()

        if group_cache[group_id].group_member_list is not None:
            for member in group_cache[group_id].group_member_list:
                member.refresh_cache()

    for user_id in user_cache:
        user_cache[user_id].refresh_cache()


def _refresh_cache_on_regular_basis():
    expire_time = config.expire_time
    while True:
        time.sleep(expire_time)
        logger.debug("开始刷新QQ信息缓存...")
        refresh_all_cache()
        logger.debug("QQ信息缓存刷新完成。")


threading.Thread(target=_refresh_cache_on_regular_basis, daemon=True).start()
