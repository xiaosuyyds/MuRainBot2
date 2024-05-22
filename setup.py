# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

import os
import sys

import requests
import bs4
import zipfile

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

# 复制./MuRainBot2/MuRainBot2-master文件到./MuRainBot2
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

lagrange_url = "https://github.com/LagrangeDev/Lagrange.Core/releases/expanded_assets/nightly"
response = requests.get(lagrange_url, proxies={'http': '127.0.0.1:10809', 'https': '127.0.0.1:10809'})
soup = bs4.BeautifulSoup(response.content.decode("utf-8"), "html.parser")
latest_release_url_ = soup.find_all("a", class_="Truncate")
latest_release_url = []
for url in latest_release_url_:
    if "Source code" not in url.find("span", class_="Truncate-text text-bold").text:
        latest_release_url.append(
            {"name": url.find("span", class_="Truncate-text text-bold").text, "url": "https://github.com" + url["href"]}
        )
print("请选择要安装的Lagrange.Core版本:")
for i, release in enumerate(latest_release_url):
    print(f"{i+1}.{release['name']}")

choice = int(input("请输入版本号: "))
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
with zipfile.ZipFile(choice["name"], 'r') as zip_ref:
    zip_ref.extractall()
os.rename(os.path.join(work_path, "publish"), onebot_path)
os.remove(choice["name"])
print("Lagrange.Core解压完成")

print("MuRainBot2安装完毕...")
