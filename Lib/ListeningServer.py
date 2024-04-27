from flask import Flask, request
from werkzeug.serving import make_server
import threading
import Lib.OnebotAPI as OnebotAPI
import Lib.Configs as Configs
import os

app = Flask(__name__)
api = OnebotAPI.OnebotAPI()

request_list = []

work_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(work_path, 'data')


# 上报
@app.route('/', methods=["POST"])
def post_data():
    data = BotController.Event(request.get_json())
    # 检测是否为重复上报
    logger.debug("收到上报: %s" % data)
    if data in request_list:
        return "ok", 204
    else:
        request_list.append(data)
    if len(request_list) > 100:
        request_list.pop(0)

    if data.post_type + '_type' in data:
        EventManager.Event((data.post_type, data[data.post_type + '_type']), data)
    else:
        EventManager.Event(data.post_type, data)

    if data.post_type == "message":
        # 私聊消息
        if data.message_type == 'private':
            message = QQRichText.QQRichText(data['message'])
            if data.sub_type == 'friend':
                logger.info("收到好友 %s(%s) 的消息: %s (%s)" % (
                    data.sender['nick_name'], data.sender['user_id'], str(message), data.message_id)
                            )
            elif data.sub_type == 'group':
                group_name = api.get("/get_group_info", {"group_id": data.group_id})["group_name"]
                logger.info("收到来自群 %s(%s) 内 %s(%s) 的临时会话消息: %s (%s)" % (
                    group_name, data.group_id,
                    data.sender['nickname'], data.sender['user_id'],
                    str(message), data.message_id
                )
                            )
            elif data.sub_type == 'other':
                logger.info("收到来自 %s(%s) 的消息: %s (%s)" % (
                    data.sender['nick_name'], data.sender['user_id'], str(message), data.message_id)
                            )

        # 群聊信息
        if data.message_type == 'group':
            user_name = data.sender['nickname']
            if data.sender['card'] != "":
                user_name = data.sender['card']
                # 了群昵称则把用户名设为群昵称
            group_name = api.get("/get_group_info", {"group_id": data.group_id})["group_name"]

            message = QQRichText.QQRichText(data.message)

            logger.info("收到群 %s(%s) 内 %s(%s) 的消息: %s (%s)" % (
                group_name, data.group_id, user_name, data.sender['user_id'], str(message),
                data.message_id))

            # 获取群文件夹路径
            group_path = os.path.join(data_path, "groups", str(data.group_id))
            # 如果获取群文件夹路径不存在，则创建
            if not os.path.exists(group_path):
                os.makedirs(group_path)

    if data.post_type == 'request':
        # 加好友邀请
        if data.request_type == 'friend':
            logger.info("收到好友 %s(%s) 的加好友邀请" % (data.sender['nickname'], data.sender['user_id']))
        # 加群邀请
        if data.request_type == 'group':
            group_name = api.get("/get_group_info", {"group_id": data.group_id})["group_name"]
            user_name = api.get("/get_stranger_info", {"user_id": data.user_id})["nickname"]
            if data.sub_type == 'invite':
                logger.info("收到来用户 %s(%s) 加入群%s(%s)的邀请" %
                            (user_name, data.user_id, group_name, data.group_id))
            elif data.sub_type == 'add':
                logger.info("收到来群%s(%s) 内 %s(%s) 加入群的请求" %
                            (group_name, data.group_id, user_name, data.user_id))

    if data.post_type == 'notice':
        if data.notice_type == 'group_upload':
            group_name = api.get("/get_group_info", {"group_id": data.group_id})["group_name"]
            logger.info("群%s(%s)内，%s上传了文件：%s" %
                        (group_name, data.group_id, data.user_id, data.file))
        # 戳一戳
        if data.notice_type == 'notify':
            group_name = api.get("/get_group_info", {"group_id": data.group_id})["group_name"]
            logger.info("收到群%s(%s)内，%s戳了戳%s" %
                        (group_name, data.group_id, data.user_id, data.target_id))

        # 进群聊
        if data.notice_type == "group_increase":
            group_name = api.get("/get_group_info", {"group_id": data.group_id})["group_name"]
            logger.info("检测到群%s(%s)内，%s进群了，操作者%s" %
                        (group_name, data.group_id, data.user_id, data.operator_id))

        # 退群聊
        if data.notice_type == "group_decrease":
            group_name = api.get("/get_group_info", {"group_id": data.group_id})["group_name"]
            user_id = data.user_id
            if data.sub_type == "leave":
                logger.info("检测到%s退出了群聊%s(%s)" % (user_id, group_name, data.group_id))
            elif data.sub_type == "kick":
                logger.info("检测到%s被%s踢出了群聊%s(%s)" % (user_id, data.operator_id, group_name, data.group_id))
            elif data.sub_type == "kick_me" or user_id == bot_uid:
                logger.info("检测到Bot被%s踢出了群聊%s(%s)" % (data.operator_id, group_name, data.group_id))

    # 若插件包含main函数则运行
    for plugin in plugins:
        try:
            if not callable(plugin["plugin"].main):
                continue
        except AttributeError:
            continue

        logger.debug("执行插件%s" % plugin["name"])
        try:
            plugin_thread = threading.Thread(
                target=plugin["plugin"].main,
                args=(
                    data.event_json,
                    work_path)
            )
            plugin_thread.start()
        except Exception as e:
            logger.error("执行插件%s时发生错误：%s" % (plugin["name"], repr(e)))
            continue

    return "ok", 204


server = make_server(Configs.GlobalConfig().server_host, Configs.GlobalConfig().server_port, app, threaded=True)
