# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|
# Code with by Xiaosu & Evan. Copyright (c) 2024 GuppyTEAM. All rights reserved.
# 本代码由校溯 和 XuFuyu编写。版权所有 （c） 2024 Guppy团队。保留所有权利。
from Lib import MuRainLib
from flask import Flask
import yaml
import os
from werkzeug.serving import make_server

logger = MuRainLib.log_init()
VERSION = "2.0.0-dev"  # 版本
VERSION_WEEK = "24Y07W"  # 版本周

app = Flask(__name__)


# 上报
@app.route('/', methods=["POST"])
def post_data():
    pass


# 导入配置文件
def import_profile(yml_path):
    try:
        with open(yml_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        profile = yaml.load(file_content, yaml.FullLoader)
        # print(content)
        logger.info("配置文件导入成功！")
        return profile
    except FileNotFoundError or OSError:
        logger.critical('配置文件导入失败！')
        return None


# 主函数
def main():
    work_path = os.path.abspath(os.path.dirname(__file__))
    yaml_path = os.path.join(work_path, 'config.yml')

    logger.info(f"MuRain Bot开始运行，当前版本：{VERSION}")
    logger.info("Code with by Xiaosu & Evan. Copyright (c) 2024 GuppyTEAM. All rights reserved.")
    logger.info("本代码由校溯 和 XuFuyu编写。版权所有 （c） 2024 Guppy团队。保留所有权利。")
    # 版本检测
    if MuRainLib.LibInfo().version == VERSION:
        logger.info("MuRainLib版本校验成功！")
    else:
        logger.warning("MuRainLib版本检测未通过，可能会发生异常\n"
                       f"MuRainLib版本:{MuRainLib.LibInfo().version} MuRain Bot版本:{VERSION}\n"
                       "注意：我们将不会受理在此模式下运行的报错")
        os.system("pause")
        logger.warning("MuRainLib版本检测未通过，可能会发生异常，将继续运行！")

    config = import_profile(yaml_path)

    logger.info("读取到监听ip，将以此ip启动监听服务器:{}:{}"
                .format(config["api"]["host"], config["api"]["port"]))

    # 启动监听服务器
    server = make_server('127.0.0.1', 5701, app)  # 此处的 host和 port对应上面 yml文件的设置
    logger.info("启动监听服务器")
    server.serve_forever()
    logger.warning("监听服务器结束运行！")


if __name__ == '__main__':
    pass
else:
    logger.warning("您当前正在使用非常规手段运行MuRain Bot，这可能会造成严重的错误！\n"
                   "注意：我们将不会受理在此模式下运行的报错")

main()
logger.warning("MuRain Bot运行结束！")
