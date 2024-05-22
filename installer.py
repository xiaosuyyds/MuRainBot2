# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

import os
import sys
import platform
import time
import select
import requests
import zipfile
import subprocess
import json

url = "https://github.com/xiaosuyyds/MuRainBot2/archive/refs/heads/master.zip"

work_path = os.path.abspath(os.path.dirname(__file__))
mrb2_path = os.path.join(work_path, "MuRainBot2")
zip_path = os.path.join(work_path, "MuRainBot2.zip")
onebot_path = os.path.join(mrb2_path, "OneBot")

if os.path.exists(mrb2_path):
    # 删除旧文件夹的所有文件
    for root, dirs, files in os.walk(mrb2_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
else:
    os.makedirs(mrb2_path)

# 增加重连接次数：
requests.DEFAULT_RETRIES = 5
s = requests.session()
# 关闭多余连接
s.keep_alive = False

print("开始下载MuRainBot2")

# 下载项目
try:
    response = requests.get(url)
    response.close()
except requests.exceptions.ProxyError:
    proxy = {'http': '127.0.0.1:10809', 'https': '127.0.0.1:10809'}
    response = requests.get(url, proxies=proxy)
    response.close()
except Exception as e:
    print("下载项目文件时遇到错误:", repr(e))
    exit()

zip_file = response.content
with open(zip_path, "wb") as f:
    f.write(zip_file)

# 解压文件
zip_file = zipfile.ZipFile(zip_path, 'r')
zip_file.extractall(mrb2_path)
zip_file.close()

# 复制所有子文件./MuRainBot2/MuRainBot2-master文件到./MuRainBot2
for root, dirs, files in os.walk(os.path.join(mrb2_path, "MuRainBot2-master")):
    for name in files:
        src = os.path.join(root, name)
        dst = os.path.join(mrb2_path, name)
        if os.path.exists(dst):
            os.remove(dst)
            print(f"删除文件: {dst}")

        os.rename(src, dst)
        print(f"移动文件: {src} -> {dst}")

    for name in dirs:
        src = os.path.join(root, name)
        dst = os.path.join(mrb2_path, name)
        if os.path.exists(dst):
            os.rmdir(dst)
            print(f"删除文件夹: {dst}")

        os.rename(src, dst)
        print(f"移动文件夹: {src} -> {dst}")
# os.remove(os.path.join(mrb2_path, "MuRainBot2-master"))

# 删除zip文件
os.remove(zip_path)
print("项目文件下载完成。")

# 安装依赖
print("开始安装依赖...")
print("如果出现错误，请检查网络连接。")
# 获取当前解释器
current_interpreter = sys.executable
# pip安装依赖
os.system("%s -m pip install -r %s" % (current_interpreter, os.path.join(mrb2_path, "requirements.txt")))

print("依赖安装完成。")

# 安装OneBot实现
print("开始安装OneBot实现...")
print("将安装LagrangeDev/Lagrange.Core")

# 由于github下载工作流附件需要登录故放弃
"""
import bs4

lagrange_url = "https://github.com/LagrangeDev/Lagrange.Core"
# 获取仓库的最新工作流
workflow_runs_url = f'{lagrange_url}/actions/workflows/Lagrange.OneBot-build.yml'
response = requests.get(workflow_runs_url, proxies={'http': '127.0.0.1:10809', 'https': '127.0.0.1:10809'})
# bs4筛选最新的工作流
soup = bs4.BeautifulSoup(response.content.decode("utf-8"), "html.parser")

latest_workflow_run = "https://github.com" + soup.find("a", class_="d-flex flex-items-center width-full mb-1")["href"]
print("最新工作流:", latest_workflow_run)

# 获取最新工作流的产物
response = requests.get(latest_workflow_run, proxies={'http': '127.0.0.1:10809', 'https': '127.0.0.1:10809'})
# bs4筛选最新的工作流产物
soup = bs4.BeautifulSoup(response.content.decode("utf-8"), "html.parser")
latest_workflow_run_artifacts = soup.find_all("a", class_="ActionListContent")
latest_workflow_run_artifacts = [artifact["href"] for artifact in latest_workflow_run_artifacts]
latest_workflow_run_artifacts = [url for url in latest_workflow_run_artifacts if "job" in url]
print("最新工作流产物:", latest_workflow_run_artifacts)
"""

lagrange_url = "https://api.github.com/repos/LagrangeDev/Lagrange.Core/releases"
response = requests.get(lagrange_url, proxies={'http': '127.0.0.1:10809', 'https': '127.0.0.1:10809'})
latest_release_url_ = response.json()[0]["assets"]
latest_release_url = []

for release in latest_release_url_:
    file = {"name": release["name"], "url": release["browser_download_url"]}
    latest_release_url.append(file)


print("请选择要安装的Lagrange.Core版本:")
for i, release in enumerate(latest_release_url):
    print(f"{i+1}.{release['name']}")

choice = input("请输入版本号（不输入将安装自动识别的版本）: ")
if choice == "":
    system = platform.system()
    cpu_architecture = platform.machine()

    if cpu_architecture == "AMD64":
        cpu_architecture = "x64"
    elif cpu_architecture == "ARM64":
        cpu_architecture = "arm64"
    elif cpu_architecture == "ARM":
        cpu_architecture = "arm"
    elif cpu_architecture == "x86":
        cpu_architecture = "x86"
    elif cpu_architecture == "x64" or cpu_architecture == "x86_64":
        cpu_architecture = "x64"

    if system == "Windows":
        system = "win"
        if cpu_architecture == "arm64":
            cpu_architecture = "x64"
        elif cpu_architecture == "arm":
            cpu_architecture = "x86"
    elif system == "Linux":
        system = "linux"
    elif system == "Darwin":
        system = "osx"
        if cpu_architecture != "arm64" and cpu_architecture != "arm":
            cpu_architecture = "x64"

    for i in range(len(latest_release_url)):
        release = latest_release_url[i]
        if system in release["name"] and cpu_architecture in release["name"]:
            choice = i + 1
            print(f"自动识别到您当前的系统是{system}，架构是{cpu_architecture}，已为您选择{release['name']}")
            break

choice = int(choice)

if choice < 1 or choice > len(latest_release_url):
    print("无效的选择")
    exit()

choice = latest_release_url[choice-1]

print("正在下载Lagrange.Core...")
response = requests.get(choice["url"], proxies={'http': '127.0.0.1:10809', 'https': '127.0.0.1:10809'})
with open(choice["name"], "wb") as f:
    f.write(response.content)

print("Lagrange.Core下载完成")

print("正在解压Lagrange.Core...")
print("Lagrange.Core解压完成")

with zipfile.ZipFile(choice["name"], 'r') as zip_ref:
    zip_ref.extractall()
os.rename(os.path.join(work_path, "publish"), onebot_path)
os.remove(choice["name"])

# 寻找Lagrange.Core的执行文件
flag = 0
lagrange_path = ""
for root, dirs, files in os.walk(onebot_path):
    for file in files:
        if "Lagrange.OneBot" in file:
            lagrange_path = os.path.join(root, file)
            flag = 1
            break
if flag == 0:
    print("未找到Lagrange.Core的执行文件")
    exit()

print("Lagrange.Core安装完成")

print("MuRainBot2安装完毕...")
print("--配置阶段--")

uid = input("请输入bot的QQ号: ")
password = input("请输入bot的密码: ")

os.chdir(onebot_path)

p = subprocess.Popen(
    lagrange_path,
    shell=True,
    stdout=subprocess.PIPE,
    stdin=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

# 获取实时输出
for line in iter(p.stdout.readline, b''):
    if "Please Edit the appsettings." in line.decode('utf-8'):
        break

p.kill()

lagrange_config_path = os.path.join(onebot_path, "appsettings.json")

# 修改配置文件
with open(lagrange_config_path, "r", encoding="utf-8") as f:
    config = json.load(f)
    config["Account"]["Uin"] = uid
    config["SignServerUrl"] = "https://sign.lagrangecore.org/api/sign"
    config["Implementations"] = [
        {
            "Type": "HttpPost",
            "Host": "127.0.0.1",
            "Port": 5701,
            "Suffix": "/",
            "HeartBeatInterval": 5000,
            "AccessToken": ""
        },
        {
            "Type": "Http",
            "Host": "127.0.0.1",
            "Port": 5700,
            "AccessToken": ""
        }
    ]
print("配置文件已修改")

with open(lagrange_config_path, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=4)

flag = 0


def login():
    global flag, uid
    print("正在进行首次登录流程...")
    p = subprocess.Popen(
        lagrange_path,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(1)
    # 获取实时输出
    for line in iter(p.stdout.readline, b''):
        if "QrCode Fetched, Expiration: 120 seconds" in line.decode('utf-8'):
            print("请扫码登陆")
            os.system("cmd.exe /c " + os.path.join(onebot_path, "qr-%s.png" % uid))
        elif "Login Success" in line.decode('utf-8'):
            print("登录成功")
            try:
                user_info = requests.get("http://127.0.0.1:5700/get_login_info").json()["data"]
                if user_info is not None:
                    user_name = user_info["nickname"]
                    uid = user_info["user_id"]
                    print("登录账号的用户名: %s(%s)" % (user_name, uid))

                    # 修改MRB2的配置文件
                    with open(os.path.join(mrb2_path, "config.yml"), "r", encoding="utf-8") as f:
                        config = f.read()
                        config = config.replace("user_id: 123456", "user_id: " + str(uid))
                        config = config.replace("nick_name: \"\"", "nick_name: \"" + user_name + "\"")

                    with open(os.path.join(mrb2_path, "config.yml"), "w", encoding="utf-8") as f:
                        f.write(config)
                else:
                    print("获取登录账号的用户信息失败")
            except Exception as e:
                print("获取登录账号的用户信息失败:", repr(e))

            flag = 1
            break
        elif "QrCode Expired, Please Fetch QrCode Again" in line.decode('utf-8'):
            print("二维码已过期，请重新扫码")
            p.kill()
            login()
            break
    p.kill()


login()

if flag == 0:
    print("登录失败，请重新运行安装程序")
    exit()
else:
    with open(lagrange_config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
        config["Account"]["Password"] = password

    with open(lagrange_config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

    print("配置文件已修改")
