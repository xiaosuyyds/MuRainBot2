# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|
"""
一个MuRainBot2的虚拟onebot实现端服务器
"""
import threading
import logging
import time

import requests
from flask import Flask, url_for, request

api_port = 5700
listening_port = 5701
login_info = {
    "user_id": 1919810114514,
    "nickname": "MuRainBot2"
}
test_environment_info = {
    "type": "group",  # private, group
    "id": 1234567890,  # 群/好友ID
    "name": "测试群",  # 群/好友昵称
    "sender_info": {
        "user_id": 11111111,
        "nickname": "测试用户",
        "card": "测试群昵称",
        "sex": "unknown",
        "age": 0,
        "join_time": 0,
        "level": 0,
        "area": "",
        "role": "member",  # owner, admin, member
        "unfriendly": False,
        "title": "测试头衔",
        "title_expire_time": -1,
        "card_changeable": False
    },
    "member_count": 2,
    "max_member_count": 2,
}

app = Flask(__name__)


def get_response(data):
    return {
        "status": "ok",
        "retcode": 0,
        "data": data
    }


now_message_id = 0


@app.route("/<node>", methods=["GET"])
def index(node):
    global now_message_id
    if node == "send_private_msg":
        user_id = request.args.get('user_id', type=int, default=None)
        message = request.args.get('message', type=str, default=None)
        if user_id is not None and message is not None:
            now_message_id += 1
            print(f"向用户{user_id}发送消息：{message}({now_message_id})")
            return get_response({"message_id": now_message_id})
        else:
            return "ok", 400
    elif node == "send_group_msg":
        group_id = request.args.get('group_id', type=int, default=None)
        message = request.args.get('message', type=str, default=None)
        if group_id is not None and message is not None:
            now_message_id += 1
            print(f"向群{group_id}发送消息：{message}({now_message_id})")
            return get_response({"message_id": now_message_id})
        else:
            return "ok", 400
    elif node == "send_msg":
        message_type = request.args.get('message_type', type=str, default=None)
        user_id = request.args.get('user_id', type=int, default=None)
        group_id = request.args.get('group_id', type=int, default=None)
        message = request.args.get('message', type=str, default=None)
        if message_type is None:
            if user_id is not None:
                message_type = "private"
            elif group_id is not None:
                message_type = "group"
            else:
                return "ok", 400
        if message_type == "private" and user_id is not None:
            req = requests.get(f"http://127.0.0.1:{api_port}/send_private_msg?user_id={user_id}&message={message}")
            return req.json(), req.status_code
        elif message_type == "group" and group_id is not None:
            req = requests.get(f"http://127.0.0.1:{api_port}/send_group_msg?group_id={group_id}&message={message}")
            return req.json(), req.status_code
        else:
            return "ok", 400
    elif node == "get_stranger_info":
        user_id = request.args.get('user_id', type=int, default=None)
        if user_id is not None:
            return get_response({
                "user_id": user_id,
                "nickname": test_environment_info["sender_info"]["nickname"],
                "remark": test_environment_info["sender_info"]["card"]
            })
        else:
            return "ok", 400
    elif node == "get_friend_list":
        return get_response([{
            "user_id": test_environment_info["sender_info"]["user_id"],
            "nickname": test_environment_info["sender_info"]["nickname"],
            "remark": test_environment_info["sender_info"]["card"]
        }])
    elif node == "get_version_info":
        return get_response({
            "app_name": "MuRainBot2",
            "app_version": "0.0.1",
            "protocol_version": "v11",
        })
    elif node == "get_group_list":
        return get_response([{
            "group_id": test_environment_info["id"],
            "group_name": test_environment_info["name"],
            "member_count": test_environment_info["member_count"],
            "max_member_count": test_environment_info["max_member_count"]
        }])
    elif node == "get_group_info":
        group_id = request.args.get('group_id', type=int, default=None)
        if group_id is not None:
            return get_response({
                "group_id": group_id,
                "group_name": test_environment_info["name"],
                "member_count": test_environment_info["member_count"],
                "max_member_count": test_environment_info["max_member_count"]
            })
        else:
            return "ok", 400
    elif node == "get_group_member_info":
        user_id = request.args.get('user_id', type=int, default=None)
        group_id = request.args.get('group_id', type=int, default=None)
        if user_id is not None and group_id is not None:
            return get_response(test_environment_info["sender_info"])
        else:
            return "ok", 400
    elif node == "get_group_member_list":
        group_id = request.args.get('group_id', type=int, default=None)
        if group_id is not None:
            return get_response([test_environment_info["sender_info"]])
        else:
            return "ok", 400
    elif node == "get_login_info":
        return get_response(login_info)
    else:
        return "ok", 404


# 启动api服务器线程
if __name__ == "__main__":
    app_run = threading.Thread(target=lambda: app.run(port=api_port), daemon=True)
    app_run.start()
    while True:
        input_message = input("请输入要发送的消息")
        now_message_id += 1

        data = {
            "time": time.time(),
            "post_type": "message",
            "self_id": login_info["user_id"],
            "message_type": test_environment_info["type"],
            "sub_type": "friend" if test_environment_info["type"] == "private" else "normal",
            "message_id": now_message_id,
            "user_id": test_environment_info["id"],
            "message": input_message,
            "raw_message": input_message,
            "font": 0,
            "sender": {
                "user_id": test_environment_info["id"],
                "nickname": test_environment_info["sender_info"]["nickname"],
                "sex": test_environment_info["sender_info"]["sex"],
                "age": test_environment_info["sender_info"]["age"]
            }
        }
        if test_environment_info["type"] == "group":
            data["group_id"] = test_environment_info["id"]
            data["user_id"] = test_environment_info["sender_info"]["user_id"]
            data["anonymous"] = None
            data["sender"]["card"] = test_environment_info["sender_info"]["card"]
            data["sender"]["area"] = test_environment_info["sender_info"]["area"]
            data["sender"]["role"] = test_environment_info["sender_info"]["role"]
            data["sender"]["level"] = test_environment_info["sender_info"]["level"]
            data["sender"]["title"] = test_environment_info["sender_info"]["title"]
        url = f"http://127.0.0.1:{listening_port}"
        requests.post(url, json=data)
