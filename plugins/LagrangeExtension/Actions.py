"""
Lagrange的拓展API接口
Tips: 下列API由Google gemini自动生成，不保证可用性
"""

from Lib import *
from Lib.core import OnebotAPI


class UploadImage(Actions.Action):
    """
    上传图片
    """
    call_func = lambda file: OnebotAPI.api.get("upload_image", {"file": file})

    def __init__(self, file: str):
        """
        Args:
            file: file 链接, 支持 http/https/file/base64
        """
        super().__init__(file=file)


class GetGroupFileUrl(Actions.Action):
    """
    获取群文件资源链接
    """
    call_func = lambda group_id, file_id, busid: OnebotAPI.api.get("get_group_file_url",
                                                                   {"group_id": group_id, "file_id": file_id,
                                                                    "busid": busid})

    def __init__(self, group_id: int, file_id: str, busid: str):
        """
        Args:
            group_id: 群 Uin
            file_id: 文件 ID
            busid: none
        """
        super().__init__(group_id=group_id, file_id=file_id, busid=busid)


class GetGroupRootFiles(Actions.Action):
    """
    获取群根目录文件列表
    """
    call_func = lambda group_id: OnebotAPI.api.get("get_group_root_files", {"group_id": group_id})

    def __init__(self, group_id: int):
        """
        Args:
            group_id: 群 Uin
        """
        super().__init__(group_id=group_id)


class GetGroupFilesByFolder(Actions.Action):
    """
    获取群子目录文件列表
    """
    call_func = lambda group_id, folder_id: OnebotAPI.api.get("get_group_files_by_folder",
                                                              {"group_id": group_id, "folder_id": folder_id})

    def __init__(self, group_id: int, folder_id: str = "/"):
        """
        Args:
            group_id: 群 Uin
            folder_id: 文件夹 ID
        """
        super().__init__(group_id=group_id, folder_id=folder_id)


class MoveGroupFile(Actions.Action):
    """
    移动群文件
    """
    call_func = lambda group_id, file_id, parent_directory, target_directory: OnebotAPI.api.get("move_group_file",
                                                                                                {"group_id": group_id,
                                                                                                 "file_id": file_id,
                                                                                                 "parent_directory": parent_directory,
                                                                                                 "target_directory": target_directory})

    def __init__(self, group_id: int, file_id: str, parent_directory: str, target_directory: str):
        """
        Args:
            group_id: 群 Uin
            file_id: 文件 ID
            parent_directory: 当前文件夹 ID
            target_directory: 目标文件夹 ID
        """
        super().__init__(group_id=group_id, file_id=file_id, parent_directory=parent_directory,
                         target_directory=target_directory)


class DeleteGroupFile(Actions.Action):
    """
    删除群文件
    """
    call_func = lambda group_id, file_id: OnebotAPI.api.get("delete_group_file",
                                                            {"group_id": group_id, "file_id": file_id})

    def __init__(self, group_id: int, file_id: str):
        """
        Args:
            group_id: 群 Uin
            file_id: 文件 ID
        """
        super().__init__(group_id=group_id, file_id=file_id)


class CreateGroupFileFolder(Actions.Action):
    """
    创建群文件文件夹
    tx不允许在非根目录创建文件夹了，该接口只能在根目录下创建文件夹
    """
    call_func = lambda group_id, name, parent_id: OnebotAPI.api.get("create_group_file_folder",
                                                                    {"group_id": group_id, "name": name,
                                                                     "parent_id": parent_id})

    def __init__(self, group_id: int, name: str, parent_id: str = "/"):
        """
        Args:
            group_id: 群 Uin
            name: 文件夹名字
            parent_id: 父文件夹 ID，tx不再允许在非根目录创建文件夹了，该值废弃，请直接传递"/"
        """
        super().__init__(group_id=group_id, name=name, parent_id=parent_id)


class DeleteGroupFileFolder(Actions.Action):
    """
    删除群文件文件夹
    """
    call_func = lambda group_id, folder_id: OnebotAPI.api.get("delete_group_file_folder",
                                                              {"group_id": group_id, "folder_id": folder_id})

    def __init__(self, group_id: int, folder_id: str):
        """
        Args:
            group_id: 群 Uin
            folder_id: 文件夹 ID
        """
        super().__init__(group_id=group_id, folder_id=folder_id)


class RenameGroupFileFolder(Actions.Action):
    """
    重命名群文件文件夹名
    """
    call_func = lambda group_id, folder_id, new_folder_name: OnebotAPI.api.get("rename_group_file_folder",
                                                                               {"group_id": group_id,
                                                                                "folder_id": folder_id,
                                                                                "new_folder_name": new_folder_name})

    def __init__(self, group_id: int, folder_id: str, new_folder_name: str):
        """
        Args:
            group_id: 群 Uin
            folder_id: 文件夹 ID
            new_folder_name: 新文件夹名称
        """
        super().__init__(group_id=group_id, folder_id=folder_id, new_folder_name=new_folder_name)


class UploadGroupFile(Actions.Action):
    """
    上传群文件
    """
    call_func = lambda group_id, file, name, folder: OnebotAPI.api.get("upload_group_file",
                                                                       {"group_id": group_id, "file": file,
                                                                        "name": name,
                                                                        "folder": folder})

    def __init__(self, group_id: int, file: str, name: str, folder: str):
        """
        Args:
            group_id: 群 Uin
            file: file 链接, 仅支持本地Path
            name: 文件名称
            folder: 文件夹 ID
        """
        super().__init__(group_id=group_id, file=file, name=name, folder=folder)


class UploadPrivateFile(Actions.Action):
    """
    上传私聊文件
    """
    call_func = lambda user_id, file, name: OnebotAPI.api.get("upload_private_file",
                                                              {"user_id": user_id, "file": file, "name": name})

    def __init__(self, user_id: int, file: str, name: str):
        """
        Args:
            user_id: 用户 Uin
            file: file 链接, 仅支持本地Path
            name: 文件名称
        """
        super().__init__(user_id=user_id, file=file, name=name)


class GetPrivateFileUrl(Actions.Action):
    """
    获取私聊文件资源链接
    """
    call_func = lambda user_id, file_id, file_hash: OnebotAPI.api.get("get_private_file_url",
                                                                      {"user_id": user_id, "file_id": file_id,
                                                                       "file_hash": file_hash})

    def __init__(self, user_id: int, file_id: str, file_hash: str = None):
        """
        Args:
            user_id: 用户 Uin，接收文件用户的Uin
            file_id: 文件 ID
            file_hash: 文件 Hash
        """
        super().__init__(user_id=user_id, file_id=file_id, file_hash=file_hash)


class FetchCustomFace(Actions.Action):
    """
    获取自定义Face
    """
    call_func = lambda: OnebotAPI.api.get("fetch_custom_face")

    def __init__(self):
        super().__init__()


class FetchMfaceKey(Actions.Action):
    """
    获取mface key
    """
    call_func = lambda emoji_ids: OnebotAPI.api.get("fetch_mface_key", {"emoji_ids": emoji_ids})

    def __init__(self, emoji_ids: list[str]):
        """
        Args:
            emoji_ids: 表情 Id 列表
        """
        super().__init__(emoji_ids=emoji_ids)


class JoinFriendEmojiChain(Actions.Action):
    """
    加入好友表情接龙
    """
    call_func = lambda user_id, message_id, emoji_id: OnebotAPI.api.get(".join_friend_emoji_chain",
                                                                        {"user_id": user_id, "message_id": message_id,
                                                                         "emoji_id": emoji_id})

    def __init__(self, user_id: int, message_id: int, emoji_id: int):
        """
        Args:
            user_id: 用户 Uin
            message_id: 期望加入表情接龙的消息id
            emoji_id: 表情id
        """
        super().__init__(user_id=user_id, message_id=message_id, emoji_id=emoji_id)


class GetAiCharacters(Actions.Action):
    """
    获取群 Ai 语音可用声色列表
    """
    call_func = lambda group_id, chat_type: OnebotAPI.api.get("get_ai_characters",
                                                              {"group_id": group_id, "chat_type": chat_type})

    def __init__(self, group_id: int = None, chat_type: int = 1):
        """
        Args:
            group_id: 群 Uin
            chat_type: 语音类型
        """
        super().__init__(group_id=group_id, chat_type=chat_type)


class JoinGroupEmojiChain(Actions.Action):
    """
    加入群聊表情接龙
    """
    call_func = lambda group_id, message_id, emoji_id: OnebotAPI.api.get(".join_group_emoji_chain",
                                                                         {"group_id": group_id,
                                                                          "message_id": message_id,
                                                                          "emoji_id": emoji_id})

    def __init__(self, group_id: int, message_id: int, emoji_id: int):
        """
        Args:
            group_id: 群号
            message_id: 期望加入表情接龙的消息id
            emoji_id: 表情id
        """
        super().__init__(group_id=group_id, message_id=message_id, emoji_id=emoji_id)


class OcrImage(Actions.Action):
    """
    OCR图像识别
    """
    call_func = lambda image: OnebotAPI.api.get("ocr_image", {"image": image})

    def __init__(self, image: str):
        """
        Args:
            image: image 链接, 支持 http/https/file/base64
        """
        super().__init__(image=image)


class SetQQAvatar(Actions.Action):
    """
    设置QQ头像
    """
    call_func = lambda file: OnebotAPI.api.get("set_qq_avatar", {"file": file})

    def __init__(self, file: str):
        """
        Args:
            file: file 链接, 支持 http/https/file/base64
        """
        super().__init__(file=file)


class DeleteFriend(Actions.Action):
    """
    删除好友
    """
    call_func = lambda user_id, block: OnebotAPI.api.get("delete_friend", {"user_id": user_id, "block": block})

    def __init__(self, user_id: str, block: bool):
        """
        Args:
            user_id: 用户 Uin
            block: 是否加入黑名单
        """
        super().__init__(user_id=user_id, block=block)


class GetRkey(Actions.Action):
    """
    获取rkey
    """
    call_func = lambda: OnebotAPI.api.get("获取rkey")

    def __init__(self):
        super().__init__()


class DelGroupNotice(Actions.Action):
    """
    删除群公告
    """
    call_func = lambda group_id, notice_id: OnebotAPI.api.get("_del_group_notice",
                                                              {"group_id": group_id, "notice_id": notice_id})

    def __init__(self, group_id: int, notice_id: str):
        """
        Args:
            group_id: 群 Uin
            notice_id: 公告 ID
        """
        super().__init__(group_id=group_id, notice_id=notice_id)


class GetAiRecord(Actions.Action):
    """
    获取群 Ai 语音
    """
    call_func = lambda character, group_id, text, chat_type: OnebotAPI.api.get("get_ai_record",
                                                                               {"character": character,
                                                                                "group_id": group_id,
                                                                                "text": text, "chat_type": chat_type})

    def __init__(self, character: str, group_id: int, text: str, chat_type: int = 1):
        """
        Args:
            character: 语音声色
            group_id: 群 Uin
            text: 语音文本
            chat_type: 语音类型
        """
        super().__init__(character=character, group_id=group_id, text=text, chat_type=chat_type)


class GetGroupNotice(Actions.Action):
    """
    获取群公告
    """
    call_func = lambda group_id: OnebotAPI.api.get("_get_group_notice", {"group_id": group_id})

    def __init__(self, group_id: int):
        """
        Args:
            group_id: 群 Uin
        """
        super().__init__(group_id=group_id)


class SetGroupBotStatus(Actions.Action):
    """
    设置群Bot发言状态
    """
    call_func = lambda group_id, bot_id, enable: OnebotAPI.api.get("set_group_bot_status",
                                                                   {"group_id": group_id, "bot_id": bot_id,
                                                                    "enable": enable})

    def __init__(self, group_id: int, bot_id: int, enable: int):
        """
        Args:
            group_id: 群 Uin
            bot_id: 机器人 Uin
            enable: 是否开启
        """
        super().__init__(group_id=group_id, bot_id=bot_id, enable=enable)


class SendGroupBotCallback(Actions.Action):
    """
    调用群机器人回调
    """
    call_func = lambda group_id, bot_id, data_1, data_2: OnebotAPI.api.get("send_group_bot_callback",
                                                                           {"group_id": group_id, "bot_id": bot_id,
                                                                            "data_1": data_1, "data_2": data_2})

    def __init__(self, group_id: int, bot_id: int, data_1: str = None, data_2: str = None):
        """
        Args:
            group_id: 群 Uin
            bot_id: 机器人 Uin
            data_1: 数据 1
            data_2: 数据 2
        """
        super().__init__(group_id=group_id, bot_id=bot_id, data_1=data_1, data_2=data_2)


class SendGroupNotice(Actions.Action):
    """
    发送群公告
    """
    call_func = lambda group_id, content, image: OnebotAPI.api.get("_send_group_notice",
                                                                   {"group_id": group_id, "content": content,
                                                                    "image": image})

    def __init__(self, group_id: int, content: str, image: str):
        """
        Args:
            group_id: 群 Uin
            content: 公告内容
            image: 公告 image 链接, 支持 http/https/file/base64
        """
        super().__init__(group_id=group_id, content=content, image=image)


class SetGroupPortrait(Actions.Action):
    """
    设置群头像
    """
    call_func = lambda group_id, file: OnebotAPI.api.get("set_group_portrait", {"group_id": group_id, "file": file})

    def __init__(self, group_id: int, file: str):
        """
        Args:
            group_id: 群 Uin
            file: file 链接, 支持 http/https/file/base64
        """
        super().__init__(group_id=group_id, file=file)


class SetGroupReaction(Actions.Action):
    """
    表情回复操作
    """
    call_func = lambda group_id, message_id, code, is_add: OnebotAPI.api.get("set_group_reaction",
                                                                             {"group_id": group_id,
                                                                              "message_id": message_id,
                                                                              "code": code, "is_add": is_add})

    def __init__(self, group_id: int, message_id: int, code: str, is_add: bool):
        """
        Args:
            group_id: 群 Uin
            message_id: 消息 ID
            code: 表情代码
            is_add: 是否是添加
        """
        super().__init__(group_id=group_id, message_id=message_id, code=code, is_add=is_add)


class DeleteEssenceMsg(Actions.Action):
    """
    删除精华消息
    """
    call_func = lambda message_id: OnebotAPI.api.get("delete_essence_msg", {"message_id": message_id})

    def __init__(self, message_id: int):
        """
        Args:
            message_id: 消息 ID
        """
        super().__init__(message_id=message_id)


class FriendPoke(Actions.Action):
    """
    私聊戳一戳
    """
    call_func = lambda user_id: OnebotAPI.api.get("friend_poke", {"user_id": user_id})

    def __init__(self, user_id: int):
        """
        Args:
            user_id: 用户 Uin
        """
        super().__init__(user_id=user_id)


class GetEssenceMsgList(Actions.Action):
    """
    获取精华消息列表
    """
    call_func = lambda group_id: OnebotAPI.api.get("get_essence_msg_list", {"group_id": group_id})

    def __init__(self, group_id: int):
        """
        Args:
            group_id: 群 Uin
        """
        super().__init__(group_id=group_id)


class GetFriendMsgHistory(Actions.Action):
    """
    获取好友历史聊天记录
    """
    call_func = lambda user_id, message_id, count: OnebotAPI.api.get("get_friend_msg_history",
                                                                     {"user_id": user_id, "message_id": message_id,
                                                                      "count": count})

    def __init__(self, user_id: int, message_id: int, count: int):
        """
        Args:
            user_id: 用户 Uin
            message_id: 消息 ID
            count: 消息数量
        """
        super().__init__(user_id=user_id, message_id=message_id, count=count)


class GetGroupMsgHistory(Actions.Action):
    """
    获取群历史聊天记录
    """
    call_func = lambda group_id, message_id, count: OnebotAPI.api.get("get_group_msg_history",
                                                                      {"group_id": group_id, "message_id": message_id,
                                                                       "count": count})

    def __init__(self, group_id: int, message_id: str, count: int = 20):
        """
        Args:
            group_id: 群 Uin
            message_id: 消息 ID
            count: 消息数量
        """
        super().__init__(group_id=group_id, message_id=message_id, count=count)


class GetMusicArk(Actions.Action):
    """
    获取音乐卡片 Json
    """
    call_func = lambda: OnebotAPI.api.get("get_music_ark")

    def __init__(self):
        super().__init__()


class GroupPoke(Actions.Action):
    """
    群里戳一戳
    """
    call_func = lambda group_id, user_id: OnebotAPI.api.get("group_poke", {"group_id": group_id, "user_id": user_id})

    def __init__(self, group_id: int, user_id: int):
        """
        Args:
            group_id: 群 Uin
            user_id: 用户 Uin
        """
        super().__init__(group_id=group_id, user_id=user_id)


class MarkMsgAsRead(Actions.Action):
    """
    标记消息为已读
    """
    call_func = lambda message_id: OnebotAPI.api.get("mark_msg_as_read", {"message_id": message_id})

    def __init__(self, message_id: int):
        """
        Args:
            message_id: 消息 ID
        """
        super().__init__(message_id=message_id)


class SendForwardMsg(Actions.Action):
    """
    构造合并转发消息
    获取的 Res Id 是属于群的, 在私聊中发送会导致图片等资源无法加载
    """
    call_func = lambda messages: OnebotAPI.api.get("send_forward_msg", {"messages": messages})

    def __init__(self, messages: list):
        """
        Args:
            messages: 消息列表
        """
        super().__init__(messages=messages)


class SendGroupAiRecord(Actions.Action):
    """
    发送群 Ai 语音
    """
    call_func = lambda character, group_id, text, chat_type: OnebotAPI.api.get("send_group_ai_record",
                                                                               {"character": character,
                                                                                "group_id": group_id,
                                                                                "text": text, "chat_type": chat_type})

    def __init__(self, character: str, group_id: int, text: str, chat_type: int = 1):
        """
        Args:
            character: 语音声色
            group_id: 群 Uin
            text: 语音文本
            chat_type: 语音类型
        """
        super().__init__(character=character, group_id=group_id, text=text, chat_type=chat_type)


class SendGroupForwardMsg(Actions.Action):
    """
    发送群聊合并转发消息
    """
    call_func = lambda group_id, messages: OnebotAPI.api.get("send_group_forward_msg",
                                                             {"group_id": group_id, "messages": messages})

    def __init__(self, group_id: int, messages: list):
        """
        Args:
            group_id: 群 Uin
            messages: 消息列表
        """
        super().__init__(group_id=group_id, messages=messages)


class SendPrivateForwardMsg(Actions.Action):
    """
    发送私聊合并转发消息
    """
    call_func = lambda user_id, messages: OnebotAPI.api.get("send_private_forward_msg",
                                                            {"user_id": user_id, "messages": messages})

    def __init__(self, user_id: int, messages: list):
        """
        Args:
            user_id: 用户 Uin
            messages: 消息列表
        """
        super().__init__(user_id=user_id, messages=messages)


class SetEssenceMsg(Actions.Action):
    """
    设置精华消息
    """
    call_func = lambda message_id: OnebotAPI.api.get("set_essence_msg", {"message_id": message_id})

    def __init__(self, message_id: int):
        """
        Args:
            message_id: 消息 ID
        """
        super().__init__(message_id=message_id)
