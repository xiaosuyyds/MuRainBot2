"""
操作
"""
import traceback

from Lib.core import OnebotAPI, ThreadPool
from Lib.utils import QQRichText, Logger

logger = Logger.get_logger()

from typing import Generic, TypeVar, Union

api = OnebotAPI.OnebotAPI()

T = TypeVar("T")  # 成功类型
E = TypeVar("E")  # 错误类型


class Result(Generic[T, E]):
    """
    结果类
    """
    def __init__(self, value: Union[T, E], is_ok: bool):
        self._value = value
        self._is_ok = is_ok

    @property
    def is_ok(self) -> bool:
        """
        判断是否成功
        Returns:
            是否成功
        """
        return self._is_ok

    @property
    def is_err(self) -> bool:
        """
        判断是否失败
        Returns:
            是否失败
        """
        return not self._is_ok

    def unwrap(self) -> T:
        """
        获取结果（如果成功，否则触发异常）
        Returns:
            结果
        """
        if self.is_ok:
            return self._value
        raise Exception(f"Called unwrap on an Err value: {self._value}")

    def unwrap_err(self) -> E:
        """
        获取错误（如果失败，否则触发异常）
        Returns:
            错误
        """
        if self.is_err:
            return self._value
        raise Exception(f"Called unwrap_err on an Ok value: {self._value}")

    def expect(self, message: str) -> T:
        """
        获取结果（如果失败，否则触发异常）
        Args:
            message: 错误信息
        Returns:
            结果
        """
        if self.is_ok:
            return self._value
        raise Exception(message)


UnCalled = type("UnCalled", (), {})


class Action:
    """
    Action基类，无实际用途，勿调用
    """
    call_func = None

    def __init__(self, *args, callback: callable = None, **kwargs):
        self._result: UnCalled | Result = UnCalled
        self._async = None
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def set_callback(self, callback: callable):
        """
        设置回调函数，如果Action已被调用则立即执行回调函数
        Returns:
            Action
        """
        self.callback = callback
        if self._result is not UnCalled:
            try:
                self.callback(self._result)
            except Exception as e:
                logger.warning(f"回调函数异常: {repr(e)}\n"
                               f"{traceback.format_exc()}")
        return self

    def call(self):
        """
        调用Action
        Returns:
            Action
        """
        try:
            result = Result(self.call_func(*self.args, **self.kwargs), True)
        except Exception as e:
            result = Result(e, False)
        self._result = result
        if self.callback is not None:
            try:
                self.callback(self._result)
            except Exception as e:
                logger.warning(f"回调函数异常: {repr(e)}\n"
                               f"{traceback.format_exc()}")
        return self

    def get_result(self) -> Result:
        """
        获取结果
        Returns:
            结果
        """
        if self._async is not None:
            self._async.result()
            self._async = None
        if self._result is UnCalled:
            raise Exception("Action not called")
        return self._result

    def call_get_result(self):
        """
        同步调用Action并获取结果
        Returns:
            结果
        """
        self.call()
        return self.get_result()

    def call_async(self):
        """
        异步调用Action
        Returns:
            Action
        """
        @ThreadPool.async_task
        def _call_async():
            return self.call()

        self._async = _call_async()
        return self

    def wait_async(self):
        """
        等待异步调用
        Returns:
            Action
        """
        if self._async is None:
            raise Exception("Action not called")
        self._async.result()
        return self


class SendPrivateMsg(Action):
    """
    发送私聊消息
    """

    call_func = api.send_private_msg

    def __init__(self, user_id: int, message: str | list[dict] | QQRichText.QQRichText):
        if isinstance(message, QQRichText.QQRichText):
            message = message.get_array()
        super().__init__(user_id=user_id, message=message)


class SendGroupMsg(Action):
    """
    发送群聊消息
    """

    call_func = api.send_group_msg

    def __init__(self, group_id: int, message: str | list[dict] | QQRichText.QQRichText):
        if isinstance(message, QQRichText.QQRichText):
            message = message.get_array()
        super().__init__(group_id=group_id, message=message)


class SendMsg(Action):
    """
    发送消息
    """

    call_func = api.send_msg

    def __init__(self, user_id: int = -1, group_id: int = -1, message: str | list[dict] | QQRichText.QQRichText = ""):
        if isinstance(message, QQRichText.QQRichText):
            message = message.get_array()

        if user_id != -1 and group_id != -1:
            raise ValueError('user_id and group_id cannot be both not -1.')
        if user_id == -1 and group_id == -1:
            raise ValueError('user_id and group_id cannot be both -1.')

        super().__init__(user_id=user_id, group_id=group_id, message=message)


class DeleteMsg(Action):
    """
    撤回消息
    """

    call_func = api.delete_msg

    def __init__(self, message_id: int):
        super().__init__(message_id=message_id)


class GetMsg(Action):
    """
    获取消息
    """

    call_func = api.get_msg

    def __init__(self, message_id: int):
        super().__init__(message_id=message_id)


class GetForwardMsg(Action):
    """
    获取合并转发消息
    """

    call_func = api.get_forward_msg

    def __init__(self, message_id: int):
        super().__init__(message_id=message_id)


class SendLike(Action):
    """
    发送好友赞
    """

    call_func = api.send_like

    def __init__(self, user_id: int, times: int = 1):
        super().__init__(user_id=user_id, times=times)


class SetGroupKick(Action):
    """
    群组踢人
    """

    call_func = api.set_group_kick

    def __init__(self, group_id: int, user_id: int, reject_add_request: bool = False):
        super().__init__(group_id=group_id, user_id=user_id, reject_add_request=reject_add_request)


class SetGroupBan(Action):
    """
    群组单人禁言
    """

    call_func = api.set_group_ban

    def __init__(self, group_id: int, user_id: int, duration: int = 30 * 60):
        super().__init__(group_id=group_id, user_id=user_id, duration=duration)


class SetGroupAnonymousBan(Action):
    """
    群组匿名用户禁言
    """

    call_func = api.set_group_anonymous_ban

    def __init__(self, group_id: int, anonymous: dict, duration: int = 30 * 60):
        super().__init__(group_id=group_id, anonymous=anonymous, duration=duration)


class SetGroupWholeBan(Action):
    """
    群组全员禁言
    """

    call_func = api.set_group_whole_ban

    def __init__(self, group_id: int, enable: bool = True):
        super().__init__(group_id=group_id, enable=enable)


class SetGroupAdmin(Action):
    """
    设置群管理员
    """

    call_func = api.set_group_admin

    def __init__(self, group_id: int, user_id: int, enable: bool = True):
        super().__init__(group_id=group_id, user_id=user_id, enable=enable)


class SetGroupCard(Action):
    """
    设置群名片（群备注）
    """

    call_func = api.set_group_card

    def __init__(self, group_id: int, user_id: int, card: str = ""):
        super().__init__(group_id=group_id, user_id=user_id, card=card)


class SetGroupLeave(Action):
    """
    退出群组
    """

    call_func = api.set_group_leave

    def __init__(self, group_id: int, is_dismiss: bool = False):
        super().__init__(group_id=group_id, is_dismiss=is_dismiss)


class SetGroupSpecialTitle(Action):
    """
    设置群组专属头衔
    """

    call_func = api.set_group_special_title

    def __init__(self, group_id: int, user_id: int, special_title: str = "", duration: int = -1):
        super().__init__(group_id=group_id, user_id=user_id, special_title=special_title, duration=duration)


class SetFriendAddRequest(Action):
    """
    处理加好友请求
    """

    call_func = api.set_friend_add_request

    def __init__(self, flag: str, approve: bool = True, remark: str = ""):
        super().__init__(flag=flag, approve=approve, remark=remark)


class SetGroupAddRequest(Action):
    """
    处理加群请求/邀请
    """

    call_func = api.set_group_add_request

    def __init__(self, flag: str, sub_type: str = "add", approve: bool = True, reason: str = ""):
        super().__init__(flag=flag, sub_type=sub_type, approve=approve, reason=reason)


class GetLoginInfo(Action):
    """
    获取登录号信息
    """

    call_func = api.get_login_info

    def __init__(self):
        super().__init__()


class GetStrangerInfo(Action):
    """
    获取陌生人信息
    """

    call_func = api.get_stranger_info

    def __init__(self, user_id: int, no_cache: bool = False):
        super().__init__(user_id=user_id, no_cache=no_cache)


class GetFriendList(Action):
    """
    获取好友列表
    """

    call_func = api.get_friend_list

    def __init__(self):
        super().__init__()


class GetGroupInfo(Action):
    """
    获取群信息
    """

    call_func = api.get_group_info

    def __init__(self, group_id: int, no_cache: bool = False):
        super().__init__(group_id=group_id, no_cache=no_cache)


class GetGroupList(Action):
    """
    获取群列表
    """

    call_func = api.get_group_list

    def __init__(self):
        super().__init__()


class GetGroupMemberInfo(Action):
    """
    获取群成员信息
    """

    call_func = api.get_group_member_info

    def __init__(self, group_id: int, user_id: int, no_cache: bool = False):
        super().__init__(group_id=group_id, user_id=user_id, no_cache=no_cache)


class GetGroupMemberList(Action):
    """
    获取群成员列表
    """

    call_func = api.get_group_member_list

    def __init__(self, group_id: int, no_cache: bool = False):
        super().__init__(group_id=group_id, no_cache=no_cache)


class GetGroupHonorInfo(Action):
    """
    获取群荣誉信息
    """

    call_func = api.get_group_honor_info

    def __init__(self, group_id: int, type_: str = "all"):
        super().__init__(group_id=group_id, type_=type_)


class GetCookies(Action):
    """
    获取 Cookies
    """

    call_func = api.get_cookies

    def __init__(self):
        super().__init__()


class GetCsrfToken(Action):
    """
    获取 CSRF Token
    """

    call_func = api.get_csrf_token

    def __init__(self):
        super().__init__()


class GetCredentials(Action):
    """
    获取 QQ 相关接口凭证
    """

    call_func = api.get_credentials

    def __init__(self):
        super().__init__()


class GetRecord(Action):
    """
    获取语音
    """

    call_func = api.get_record

    def __init__(self, file: str, out_format: str = "mp3", out_file: str = ""):
        super().__init__(file=file, out_format=out_format, out_file=out_file)


class GetImage(Action):
    """
    获取图片
    """

    call_func = api.get_image

    def __init__(self, file: str):
        super().__init__(file=file)


class CanSendImage(Action):
    """
    检查是否可以发送图片
    """

    call_func = api.can_send_image

    def __init__(self):
        super().__init__()


class CanSendRecord(Action):
    """
    检查是否可以发送语音
    """

    call_func = api.can_send_record

    def __init__(self):
        super().__init__()


class GetStatus(Action):
    """
    获取运行状态
    """

    call_func = api.get_status

    def __init__(self):
        super().__init__()


class GetVersionInfo(Action):
    """
    获取版本信息
    """

    call_func = api.get_version_info

    def __init__(self):
        super().__init__()


class SetRestart(Action):
    """
    重启
    """

    call_func = api.set_restart

    def __init__(self, delay: int = 0):
        super().__init__(delay=delay)


class CleanCache(Action):
    """
    清理缓存
    """

    call_func = api.clean_cache

    def __init__(self):
        super().__init__()


"""
使用示例：

if __name__ == "__main__":
    ThreadPool.init()

    action = SendPrivateMsg(user_id=123456789, message="Hello World").call()
    res = action.get_result()

    # 下面二者等价
    res = SendPrivateMsg(user_id=123456789, message="Hello World").call().get_result()
    res = SendPrivateMsg(user_id=123456789, message="Hello World").call_get_result()

    action = SendPrivateMsg(user_id=123456789, message="Hello World").call_async()
    res = action.get_result()

    if res.is_ok:
        print(res.unwrap())
    else:
        print(res.unwrap_err())
"""
