"""
Lagrange的拓展API接口
Tips: 下列API由Google gemini自动生成，不保证可用性
"""

from typing import Callable

from Lib.core import OnebotAPI
from Lib import Actions


class UploadImage(Actions.Action):
    """
    上传图片
    """

    def call_func(self, file: str):
        return OnebotAPI.api.get("upload_image", {"file": file})

    def __init__(self, file: str, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            file: file 链接, 支持 http/https/file/base64
            callback: 回调函数
        """
        super().__init__(file=file, callback=callback)


class GetGroupFileUrl(Actions.Action):
    """
    获取群文件资源链接
    """

    def call_func(self, group_id: int, file_id: str, busid: str):
        return OnebotAPI.api.get("get_group_file_url",
                                 {"group_id": group_id, "file_id": file_id,
                                  "busid": busid})

    def __init__(self, group_id: int, file_id: str, busid: str, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            file_id: 文件 ID
            busid: none
            callback: 回调函数
        """
        super().__init__(group_id=group_id, file_id=file_id, busid=busid, callback=callback)


class GetGroupRootFiles(Actions.Action):
    """
    获取群根目录文件列表
    """

    def call_func(self, group_id: int):
        return OnebotAPI.api.get("get_group_root_files", {"group_id": group_id})

    def __init__(self, group_id: int, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            callback: 回调函数
        """
        super().__init__(group_id=group_id, callback=callback)


class GetGroupFilesByFolder(Actions.Action):
    """
    获取群子目录文件列表
    """

    def call_func(self, group_id: int, folder_id: str):
        return OnebotAPI.api.get("get_group_files_by_folder",
                                 {"group_id": group_id, "folder_id": folder_id})

    def __init__(self, group_id: int, folder_id: str = "/", callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            folder_id: 文件夹 ID
            callback: 回调函数
        """
        super().__init__(group_id=group_id, folder_id=folder_id, callback=callback)


class MoveGroupFile(Actions.Action):
    """
    移动群文件
    """

    def call_func(self, group_id: int, file_id: str, parent_directory: str, target_directory: str):
        return OnebotAPI.api.get(
            "move_group_file",
            {"group_id": group_id,
             "file_id": file_id,
             "parent_directory": parent_directory,
             "target_directory": target_directory})

    def __init__(self, group_id: int, file_id: str, parent_directory: str, target_directory: str,
                 callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            file_id: 文件 ID
            parent_directory: 当前文件夹 ID
            target_directory: 目标文件夹 ID
            callback: 回调函数
        """
        super().__init__(group_id=group_id, file_id=file_id, parent_directory=parent_directory,
                         target_directory=target_directory, callback=callback)


class DeleteGroupFile(Actions.Action):
    """
    删除群文件
    """

    def call_func(self, group_id: int, file_id: str):
        return OnebotAPI.api.get("delete_group_file",
                                 {"group_id": group_id, "file_id": file_id})

    def __init__(self, group_id: int, file_id: str, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            file_id: 文件 ID
            callback: 回调函数
        """
        super().__init__(group_id=group_id, file_id=file_id, callback=callback)


class CreateGroupFileFolder(Actions.Action):
    """
    创建群文件文件夹
    tx不允许在非根目录创建文件夹了，该接口只能在根目录下创建文件夹
    """

    def call_func(self, group_id: int, name: str, parent_id: str):
        return OnebotAPI.api.get("create_group_file_folder",
                                 {"group_id": group_id, "name": name,
                                  "parent_id": parent_id})

    def __init__(self, group_id: int, name: str, parent_id: str = "/",
                 callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            name: 文件夹名字
            parent_id: 父文件夹 ID，tx不再允许在非根目录创建文件夹了，该值废弃，请直接传递"/"
            callback: 回调函数
        """
        super().__init__(group_id=group_id, name=name, parent_id=parent_id, callback=callback)


class DeleteGroupFileFolder(Actions.Action):
    """
    删除群文件文件夹
    """

    def call_func(self, group_id: int, folder_id: str):
        return OnebotAPI.api.get("delete_group_file_folder",
                                 {"group_id": group_id, "folder_id": folder_id})

    def __init__(self, group_id: int, folder_id: str, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            folder_id: 文件夹 ID
            callback: 回调函数
        """
        super().__init__(group_id=group_id, folder_id=folder_id, callback=callback)


class RenameGroupFileFolder(Actions.Action):
    """
    重命名群文件文件夹名
    """

    def call_func(self, group_id: int, folder_id: str, new_folder_name: str):
        return OnebotAPI.api.get("rename_group_file_folder",
                                 {"group_id": group_id,
                                  "folder_id": folder_id,
                                  "new_folder_name": new_folder_name})

    def __init__(self, group_id: int, folder_id: str, new_folder_name: str,
                 callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            folder_id: 文件夹 ID
            new_folder_name: 新文件夹名称
            callback: 回调函数
        """
        super().__init__(group_id=group_id, folder_id=folder_id, new_folder_name=new_folder_name, callback=callback)


class UploadGroupFile(Actions.Action):
    """
    上传群文件
    """

    def call_func(self, group_id: int, file: str, name: str, folder: str):
        return OnebotAPI.api.get("upload_group_file",
                                 {"group_id": group_id, "file": file,
                                  "name": name,
                                  "folder": folder})

    def __init__(self, group_id: int, file: str, name: str, folder: str,
                 callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            file: file 链接, 仅支持本地Path
            name: 文件名称
            folder: 文件夹 ID
            callback: 回调函数
        """
        super().__init__(group_id=group_id, file=file, name=name, folder=folder, callback=callback)


class UploadPrivateFile(Actions.Action):
    """
    上传私聊文件
    """

    def call_func(self, user_id: int, file: str, name: str):
        return OnebotAPI.api.get("upload_private_file",
                                 {"user_id": user_id, "file": file, "name": name})

    def __init__(self, user_id: int, file: str, name: str, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            user_id: 用户 Uin
            file: file 链接, 仅支持本地Path
            name: 文件名称
            callback: 回调函数
        """
        super().__init__(user_id=user_id, file=file, name=name, callback=callback)


class GetPrivateFileUrl(Actions.Action):
    """
    获取私聊文件资源链接
    """

    def call_func(self, user_id: int, file_id: str, file_hash: str):
        return OnebotAPI.api.get("get_private_file_url",
                                 {"user_id": user_id, "file_id": file_id,
                                  "file_hash": file_hash})

    def __init__(self, user_id: int, file_id: str, file_hash: str = None,
                 callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            user_id: 用户 Uin，接收文件用户的Uin
            file_id: 文件 ID
            file_hash: 文件 Hash
            callback: 回调函数
        """
        super().__init__(user_id=user_id, file_id=file_id, file_hash=file_hash, callback=callback)


class FetchCustomFace(Actions.Action):
    """
    获取自定义Face
    """

    def call_func(self):
        return OnebotAPI.api.get("fetch_custom_face")

    def __init__(self, callback: Callable[[Actions.Result], ...] = None):
        super().__init__(callback=callback)


class FetchMfaceKey(Actions.Action):
    """
    获取mface key
    """

    def call_func(self, emoji_ids: list[str]):
        return OnebotAPI.api.get("fetch_mface_key", {"emoji_ids": emoji_ids})

    def __init__(self, emoji_ids: list[str], callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            emoji_ids: 表情 Id 列表
            callback: 回调函数
        """
        super().__init__(emoji_ids=emoji_ids, callback=callback)


class JoinFriendEmojiChain(Actions.Action):
    """
    加入好友表情接龙
    """

    def call_func(self, user_id: int, message_id: int, emoji_id: int):
        return OnebotAPI.api.get(".join_friend_emoji_chain",
                                 {"user_id": user_id, "message_id": message_id,
                                  "emoji_id": emoji_id})

    def __init__(self, user_id: int, message_id: int, emoji_id: int, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            user_id: 用户 Uin
            message_id: 期望加入表情接龙的消息id
            emoji_id: 表情id
            callback: 回调函数
        """
        super().__init__(user_id=user_id, message_id=message_id, emoji_id=emoji_id, callback=callback)


class GetAiCharacters(Actions.Action):
    """
    获取群 Ai 语音可用声色列表
    """

    def call_func(self, group_id: int, chat_type: int):
        return OnebotAPI.api.get("get_ai_characters",
                                 {"group_id": group_id, "chat_type": chat_type})

    def __init__(self, group_id: int = None, chat_type: int = 1, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            chat_type: 语音类型
            callback: 回调函数
        """
        super().__init__(group_id=group_id, chat_type=chat_type, callback=callback)


class JoinGroupEmojiChain(Actions.Action):
    """
    加入群聊表情接龙
    """

    def call_func(self, group_id: int, message_id: int, emoji_id: int):
        return OnebotAPI.api.get(".join_group_emoji_chain",
                                 {"group_id": group_id,
                                  "message_id": message_id,
                                  "emoji_id": emoji_id})

    def __init__(self, group_id: int, message_id: int, emoji_id: int, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群号
            message_id: 期望加入表情接龙的消息id
            emoji_id: 表情id
            callback: 回调函数
        """
        super().__init__(group_id=group_id, message_id=message_id, emoji_id=emoji_id, callback=callback)


class OcrImage(Actions.Action):
    """
    OCR图像识别
    """

    def call_func(self, image: str):
        return OnebotAPI.api.get("ocr_image", {"image": image})

    def __init__(self, image: str, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            image: image 链接, 支持 http/https/file/base64
            callback: 回调函数
        """
        super().__init__(image=image, callback=callback)


class SetQQAvatar(Actions.Action):
    """
    设置QQ头像
    """

    def call_func(self, file: str):
        return OnebotAPI.api.get("set_qq_avatar", {"file": file})

    def __init__(self, file: str, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            file: file 链接, 支持 http/https/file/base64
            callback: 回调函数
        """
        super().__init__(file=file, callback=callback)


class DeleteFriend(Actions.Action):
    """
    删除好友
    """

    def call_func(self, user_id: str, block: bool):
        return OnebotAPI.api.get("delete_friend", {"user_id": user_id, "block": block})

    def __init__(self, user_id: str, block: bool, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            user_id: 用户 Uin
            block: 是否加入黑名单
            callback: 回调函数
        """
        super().__init__(user_id=user_id, block=block, callback=callback)


class GetRkey(Actions.Action):
    """
    获取rkey
    """

    def call_func(self):
        return OnebotAPI.api.get("获取rkey")

    def __init__(self, callback: Callable[[Actions.Result], ...] = None):
        super().__init__(callback=callback)


class DelGroupNotice(Actions.Action):
    """
    删除群公告
    """

    def call_func(self, group_id: int, notice_id: str):
        return OnebotAPI.api.get("_del_group_notice",
                                 {"group_id": group_id, "notice_id": notice_id})

    def __init__(self, group_id: int, notice_id: str, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            notice_id: 公告 ID
            callback: 回调函数
        """
        super().__init__(group_id=group_id, notice_id=notice_id, callback=callback)


class GetAiRecord(Actions.Action):
    """
    获取群 Ai 语音
    """

    def call_func(self, character: str, group_id: int, text: str, chat_type: int):
        return OnebotAPI.api.get("get_ai_record",
                                 {"character": character,
                                  "group_id": group_id,
                                  "text": text, "chat_type": chat_type})

    def __init__(self, character: str, group_id: int, text: str, chat_type: int = 1,
                 callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            character: 语音声色
            group_id: 群 Uin
            text: 语音文本
            chat_type: 语音类型
            callback: 回调函数
        """
        super().__init__(character=character, group_id=group_id, text=text, chat_type=chat_type, callback=callback)


class GetGroupNotice(Actions.Action):
    """
    获取群公告
    """

    def call_func(self, group_id: int):
        return OnebotAPI.api.get("_get_group_notice", {"group_id": group_id})

    def __init__(self, group_id: int, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            callback: 回调函数
        """
        super().__init__(group_id=group_id, callback=callback)


class SetGroupBotStatus(Actions.Action):
    """
    设置群Bot发言状态
    """

    def call_func(self, group_id: int, bot_id: int, enable: int):
        return OnebotAPI.api.get("set_group_bot_status",
                                 {"group_id": group_id, "bot_id": bot_id,
                                  "enable": enable})

    def __init__(self, group_id: int, bot_id: int, enable: int, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            bot_id: 机器人 Uin
            enable: 是否开启
            callback: 回调函数
        """
        super().__init__(group_id=group_id, bot_id=bot_id, enable=enable, callback=callback)


class SendGroupBotCallback(Actions.Action):
    """
    调用群机器人回调
    """

    def call_func(self, group_id: int, bot_id: int, data_1: str, data_2: str):
        return OnebotAPI.api.get("send_group_bot_callback",
                                 {"group_id": group_id, "bot_id": bot_id,
                                  "data_1": data_1, "data_2": data_2})

    def __init__(self, group_id: int, bot_id: int, data_1: str = None, data_2: str = None,
                 callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            bot_id: 机器人 Uin
            data_1: 数据 1
            data_2: 数据 2
            callback: 回调函数
        """
        super().__init__(group_id=group_id, bot_id=bot_id, data_1=data_1, data_2=data_2, callback=callback)


class SendGroupNotice(Actions.Action):
    """
    发送群公告
    """

    def call_func(self, group_id: int, content: str, image: str):
        return OnebotAPI.api.get("_send_group_notice",
                                 {"group_id": group_id, "content": content,
                                  "image": image})

    def __init__(self, group_id: int, content: str, image: str, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            content: 公告内容
            image: 公告 image 链接, 支持 http/https/file/base64
            callback: 回调函数
        """
        super().__init__(group_id=group_id, content=content, image=image, callback=callback)


class SetGroupPortrait(Actions.Action):
    """
    设置群头像
    """

    def call_func(self, group_id: int, file: str):
        return OnebotAPI.api.get("set_group_portrait", {"group_id": group_id, "file": file})

    def __init__(self, group_id: int, file: str, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            file: file 链接, 支持 http/https/file/base64
            callback: 回调函数
        """
        super().__init__(group_id=group_id, file=file, callback=callback)


class SetGroupReaction(Actions.Action):
    """
    表情回复操作
    """

    def call_func(self, group_id, message_id, code, is_add):
        return OnebotAPI.api.get("set_group_reaction",
                                 {"group_id": group_id,
                                  "message_id": message_id,
                                  "code": code, "is_add": is_add})

    def __init__(self, group_id: int, message_id: int, code: str, is_add: bool,
                 callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            message_id: 消息 ID
            code: 表情代码
            is_add: 是否是添加
            callback: 回调函数
        """
        super().__init__(group_id=group_id, message_id=message_id, code=code, is_add=is_add, callback=callback)


class DeleteEssenceMsg(Actions.Action):
    """
    删除精华消息
    """

    def call_func(self, message_id: int):
        return OnebotAPI.api.get("delete_essence_msg", {"message_id": message_id})

    def __init__(self, message_id: int, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            message_id: 消息 ID
            callback: 回调函数
        """
        super().__init__(message_id=message_id, callback=callback)


class FriendPoke(Actions.Action):
    """
    私聊戳一戳
    """

    def call_func(self, user_id: int):
        return OnebotAPI.api.get("friend_poke", {"user_id": user_id})

    def __init__(self, user_id: int, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            user_id: 用户 Uin
            callback: 回调函数
        """
        super().__init__(user_id=user_id, callback=callback)


class GetEssenceMsgList(Actions.Action):
    """
    获取精华消息列表
    """

    def call_func(self, group_id: int):
        return OnebotAPI.api.get("get_essence_msg_list", {"group_id": group_id})

    def __init__(self, group_id: int, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            callback: 回调函数
        """
        super().__init__(group_id=group_id, callback=callback)


class GetFriendMsgHistory(Actions.Action):
    """
    获取好友历史聊天记录
    """

    def call_func(self, user_id: int, message_id: int, count: int):
        return OnebotAPI.api.get("get_friend_msg_history",
                                 {"user_id": user_id, "message_id": message_id,
                                  "count": count})

    def __init__(self, user_id: int, message_id: int, count: int, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            user_id: 用户 Uin
            message_id: 消息 ID
            count: 消息数量
            callback: 回调函数
        """
        super().__init__(user_id=user_id, message_id=message_id, count=count, callback=callback)


class GetGroupMsgHistory(Actions.Action):
    """
    获取群历史聊天记录
    """

    def call_func(self, group_id: int, message_id: str, count: int):
        return OnebotAPI.api.get("get_group_msg_history",
                                 {"group_id": group_id, "message_id": message_id,
                                  "count": count})

    def __init__(self, group_id: int, message_id: str, count: int = 20,
                 callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            message_id: 消息 ID
            count: 消息数量
            callback: 回调函数
        """
        super().__init__(group_id=group_id, message_id=message_id, count=count, callback=callback)


class GetMusicArk(Actions.Action):
    """
    获取音乐卡片 Json
    """

    def call_func(self):
        return OnebotAPI.api.get("get_music_ark")

    def __init__(self, callback: Callable[[Actions.Result], ...] = None):
        super().__init__(callback=callback)


class GroupPoke(Actions.Action):
    """
    群里戳一戳
    """

    def call_func(self, group_id: int, user_id: int):
        return OnebotAPI.api.get("group_poke", {"group_id": group_id, "user_id": user_id})

    def __init__(self, group_id: int, user_id: int, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            user_id: 用户 Uin
            callback: 回调函数
        """
        super().__init__(group_id=group_id, user_id=user_id, callback=callback)


class MarkMsgAsRead(Actions.Action):
    """
    标记消息为已读
    """

    def call_func(self, message_id: int):
        return OnebotAPI.api.get("mark_msg_as_read", {"message_id": message_id})

    def __init__(self, message_id: int, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            message_id: 消息 ID
            callback: 回调函数
        """
        super().__init__(message_id=message_id, callback=callback)


class SendForwardMsg(Actions.Action):
    """
    构造合并转发消息
    获取的 Res Id 是属于群的, 在私聊中发送会导致图片等资源无法加载
    """

    def call_func(self, messages: list):
        return OnebotAPI.api.get("send_forward_msg", {"messages": messages})

    def __init__(self, messages: list, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            messages: 消息列表
            callback: 回调函数
        """
        super().__init__(messages=messages, callback=callback)


class SendGroupAiRecord(Actions.Action):
    """
    发送群 Ai 语音
    """

    def call_func(self, character: str, group_id: int, text: str, chat_type: int):
        return OnebotAPI.api.get("send_group_ai_record",
                                 {"character": character,
                                  "group_id": group_id,
                                  "text": text, "chat_type": chat_type})

    def __init__(self, character: str, group_id: int, text: str, chat_type: int = 1,
                 callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            character: 语音声色
            group_id: 群 Uin
            text: 语音文本
            chat_type: 语音类型
            callback: 回调函数
        """
        super().__init__(character=character, group_id=group_id, text=text, chat_type=chat_type, callback=callback)


class SendGroupForwardMsg(Actions.Action):
    """
    发送群聊合并转发消息
    """

    def call_func(self, group_id: int, messages: list):
        return OnebotAPI.api.get("send_group_forward_msg",
                                 {"group_id": group_id, "messages": messages})

    def __init__(self, group_id: int, messages: list, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            group_id: 群 Uin
            messages: 消息列表
            callback: 回调函数
        """
        super().__init__(group_id=group_id, messages=messages, callback=callback)


class SendPrivateForwardMsg(Actions.Action):
    """
    发送私聊合并转发消息
    """

    def call_func(self, user_id: int, messages: list):
        return OnebotAPI.api.get("send_private_forward_msg",
                                 {"user_id": user_id, "messages": messages})

    def __init__(self, user_id: int, messages: list, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            user_id: 用户 Uin
            messages: 消息列表
            callback: 回调函数
        """
        super().__init__(user_id=user_id, messages=messages, callback=callback)


class SetEssenceMsg(Actions.Action):
    """
    设置精华消息
    """

    def call_func(self, message_id: int):
        return OnebotAPI.api.get("set_essence_msg", {"message_id": message_id})

    def __init__(self, message_id: int, callback: Callable[[Actions.Result], ...] = None):
        """
        Args:
            message_id: 消息 ID
            callback: 回调函数
        """
        super().__init__(message_id=message_id, callback=callback)
