#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

from tqdm import tqdm
import os
import platform
import time
import requests
import zipfile
import subprocess
import json
import shutil
import multitasking
import sys
from retry import retry

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
    proxy = {'http': '127.0.0.1:10809', 'https': '127.0.0.1:10809'}
    with open(zip_path, "wb") as f, requests.get(url, stream=True, proxies=proxy) as res:
        with tqdm(total=int(res.headers.get('content-length', 0)), unit='iB', unit_scale=True) as pbar:
            for chunk in res.iter_content(chunk_size=64 * 1024):
                if not chunk:
                    break
                f.write(chunk)
                pbar.update(len(chunk))
except Exception as e:
    print("下载项目文件时遇到错误:", repr(e))
    exit()

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
os.system("{} -m pip install -r {}".format(current_interpreter, os.path.join(mrb2_path, "requirements.txt")))

print("依赖安装完成。")
print("MuRainBot2安装完毕...\n\n")

print("接下来将安装OneBot实现，感谢xiaosuyyds/Lagrange.Installer提供的安装代码（虽然这个代码也是我写的www）")


proxies = {'http': '127.0.0.1:10809', 'https': '127.0.0.1:10809'}
# proxies = None

# 定义 1 MB 多少为 B
MB = 1024 ** 2

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

onebot_path = os.path.join(mrb2_path, "OneBot")


def split(_: int, end: int, step: int) -> list[tuple[int, int]]:
    if end == 0:
        raise ValueError("end 值不能为0")
    parts = [(start, min(start + step, end)) for start in range(0, end, step)]
    return parts


def download(url: str, file_name: str, retry_times: int = 3,
             each_size: int = 15 * MB, silent_installation: bool = False) -> None:
    """
    根据文件直链和文件名下载文件

    Parameters
    ----------
    :param url : 文件直链
    :param file_name : 文件名
    :param retry_times: 可选的，每次连接失败重试次数
    :param param each_size: 可选的，每次下载的大小，默认为 3MB
    :param silent_installation: 可选的，是否静默安装
    Return
    ------
    None


    """
    f = open(file_name, 'wb')
    file_size = get_file_size(url)

    @retry(tries=retry_times)
    @multitasking.task
    def start_download(start: int, end: int) -> None:
        """
        根据文件起止位置下载文件

        Parameters
        ----------
        start : 开始位置
        end : 结束位置
        """
        _headers = headers.copy()
        # 分段下载的核心
        _headers['Range'] = f'bytes={start}-{end}'
        # 发起请求并获取响应（流式）
        response = session.get(url, headers=_headers, stream=True, proxies=proxies)
        # 每次读取的流式响应大小
        chunk_size = 128
        # 暂存已获取的响应，后续循环写入
        chunks = []
        for chunk in response.iter_content(chunk_size=chunk_size):
            # 暂存获取的响应
            chunks.append(chunk)
            if not silent_installation:
                # 更新进度条
                bar.update(chunk_size)
        f.seek(start)
        for chunk in chunks:
            f.write(chunk)
        # 释放已写入的资源
        del chunks

    session = requests.Session()
    # 分块文件如果比文件大，就取文件大小为分块大小
    each_size = min(each_size, file_size)

    # 分块
    parts = split(0, file_size, each_size)
    if not silent_installation:
        print(f'分块数：{len(parts)}')

    bar = None
    if not silent_installation:
        # 创建进度条
        bar = tqdm(total=file_size, desc=f'正在下载', unit='B', unit_scale=True, leave=True)

    for part in parts:
        start, end = part
        start_download(start, end)
    # 等待全部线程结束
    multitasking.wait_for_tasks()
    f.close()

    if not silent_installation:
        bar.close()


def get_file_size(url: str) -> int:
    """
    获取文件大小

    Parameters
    ----------
    url : 文件直链

    Return
    ------
    文件大小（B为单位）
    如果不支持则会报错

    """
    response = requests.head(url, proxies=proxies)
    file_size = response.headers.get('content-length', 0)
    if file_size is None:
        raise ValueError('该文件不支持多线程分段下载！')
    return int(file_size)


def install(silent_installation: bool = False):
    if not silent_installation:
        # 检查OneBot是否已经存在
        if os.path.exists(onebot_path):
            if input("OneBot文件夹已经存在，是否删除？(y/n): ").lower() == "y":
                try:
                    shutil.rmtree(onebot_path)
                    print("已删除OneBot文件夹。休对故人思故国，且将新火试新茶。")
                except PermissionError as e:
                    if "[WinError 32]" in str(e):
                        print("无法删除OneBot文件夹，文件被占用，请尝试重启电脑等方式: " + repr(e))
                    else:
                        print("删除OneBot文件夹时发生未知错误: " + repr(e))
                    sys.exit()
                except Exception as e:
                    print("删除OneBot文件夹时发生未知错误: " + repr(e))
                    sys.exit()
            else:
                print("已取消安装")
                sys.exit()
            print()
    else:
        if os.path.exists(onebot_path):
            shutil.rmtree(onebot_path)

    # 下载Lagrange.Core
    if not silent_installation:
        print("准备安装LagrangeDev/Lagrange.Core")

    # 增加重连接次数：
    requests.DEFAULT_RETRIES = 5
    s = requests.session()
    # 关闭多余连接
    s.keep_alive = False

    # 由于github下载工作流附件需要登录故放弃
    """
    import bs4

    lagrange_url = "https://github.com/LagrangeDev/Lagrange.Core"
    # 获取仓库的最新工作流
    workflow_runs_url = f'{lagrange_url}/actions/workflows/Lagrange.OneBot-build.yml'
    response = requests.get(workflow_runs_url, proxies=proxies)
    # bs4筛选最新的工作流
    soup = bs4.BeautifulSoup(response.content.decode("utf-8"), "html.parser")

    latest_workflow_run = ("https://github.com" + 
                           soup.find("a", class_="d-flex flex-items-center width-full mb-1")["href"])
    print("最新工作流:", latest_workflow_run)

    # 获取最新工作流的产物
    response = requests.get(latest_workflow_run, proxies=proxies)
    # bs4筛选最新的工作流产物
    soup = bs4.BeautifulSoup(response.content.decode("utf-8"), "html.parser")
    latest_workflow_run_artifacts = soup.find_all("a", class_="ActionListContent")
    latest_workflow_run_artifacts = [artifact["href"] for artifact in latest_workflow_run_artifacts]
    latest_workflow_run_artifacts = [url for url in latest_workflow_run_artifacts if "job" in url]
    print("最新工作流产物:", latest_workflow_run_artifacts)
    """

    # 获取Lagrange.Core最新版本
    lagrange_url = "https://api.github.com/repos/LagrangeDev/Lagrange.Core/releases"
    response = requests.get(lagrange_url, proxies=proxies)
    if response.status_code != 200:
        print("获取Lagrange.Core最新版本失败，请检查网络连接或稍后重试")
        sys.exit()
    latest_release_url = response.json()[0]["assets"]
    if not silent_installation:
        print("请选择要安装的Lagrange.Onebot版本:")
        for i, release in enumerate(latest_release_url):
            print(f"{i + 1}.{release['name']}")

        choice = input("请输入版本号（不输入将安装自动识别的版本）: ")
    else:
        choice = ""

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
                if not silent_installation:
                    print(
                        f"自动识别到您当前的系统是{platform.system()}，架构是{platform.machine()}，已为您选择{release['name']}")
                break

    choice = int(choice)

    if choice < 1 or choice > len(latest_release_url):
        print("无效的选择")
        sys.exit()

    choice = latest_release_url[choice - 1]

    zip_path = str(os.path.join(work_path, choice["name"]))

    flag = True
    if not silent_installation:
        print("海内存知己，天涯若比邻。正在为你下载Lagrange.Onebot，请稍等...")

    # github在下载链接里有一层跳转，如果不这么写会无法获取下载的文件大小
    choice["browser_download_url"] = requests.head(choice["browser_download_url"],
                                                   proxies=proxies).headers.get("location", 0)

    for _ in range(3):
        download(choice["browser_download_url"], zip_path, silent_installation=silent_installation)
        if not silent_installation:
            print("Lagrange.Onebot下载完成\n")

            print("正在解压Lagrange.Onebot...")

        try:
            zip_file = zipfile.ZipFile(zip_path)
            for names in zip_file.namelist():
                zip_file.extract(names, onebot_path)
            zip_file.close()
            flag = False
            break
        except Exception as e:
            if not silent_installation:
                print("解压失败，报错: %s正在重新下载...\n" % repr(e))
            continue

    if flag:
        if not silent_installation:
            print("已达重试上线，请尝试重新运行此程序")
        sys.exit()

    os.remove(zip_path)
    if not silent_installation:
        print("Lagrange.Onebot解压完成\n")

    # 寻找Lagrange.Onebot的执行文件
    flag = 0
    lagrange_path = ""
    for root, dirs, files in os.walk(os.path.join(onebot_path, "publish")):
        for file in files:
            if "Lagrange.OneBot" in file:
                lagrange_path = os.path.join(root, file)
                flag = 1
                break

    if flag == 0:
        if not silent_installation:
            print("未找到Lagrange.Onebot的执行文件")
        sys.exit()

    os.rename(lagrange_path, os.path.join(onebot_path, os.path.basename(lagrange_path)))
    lagrange_path = os.path.join(onebot_path, os.path.basename(lagrange_path))
    os.rmdir(os.path.join(onebot_path, "publish"))
    return lagrange_path


def arrangement(lagrange_path: str, silent_installation: bool = False, uid: int = None, password: str = None):
    if not silent_installation:
        uid = input("请输入bot的QQ号(不输入则请勾选“下次登录无需确认”): ")
        password = input("请输入bot的密码(不输入则请勾选“下次登录无需确认”): ")

        if uid == "":
            uid = 0
        try:
            uid = int(uid)
        except ValueError:
            print("QQ号必须为数字")
            sys.exit()

    if uid is None:
        uid = 0

    if password is None:
        password = ""

    os.chdir(onebot_path)

    # 先运行一下Lagrange.Onebot，以生成配置文件
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

    if platform.system() == "Windows":
        # 获取pid
        pid = p.pid

        # 结束进程
        os.system("taskkill /F /T /PID %d" % pid)
    else:
        p.kill()

    lagrange_config_path = os.path.join(onebot_path, "appsettings.json")

    # 修改配置文件
    with open(lagrange_config_path, "r+", encoding="utf-8") as f:
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
        f.seek(0)
        json.dump(config, f, ensure_ascii=False, indent=4)

    if not silent_installation:
        print("配置文件修改完毕！\n与君初相识，犹如故人归。\n")

    def login(uid):
        flag = 0
        print("一切即将准备就绪，正在进行首次登录流程，请不要结束进程...")
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
                flag = 1
                print("登录成功，有朋自远方来，不亦乐乎。")
                try:
                    user_info = requests.get("http://127.0.0.1:5700/get_login_info").json()["data"]
                    if user_info is not None:
                        user_name = user_info["nickname"]
                        uid = user_info["user_id"]
                        print(f"登录账号的用户名: {user_name}({uid})")
                    else:
                        print("获取登录账号的用户信息失败")
                except Exception as e:
                    print("获取登录账号的用户信息失败:", repr(e))
                break
            elif "QrCode Expired, Please Fetch QrCode Again" in line.decode('utf-8'):
                print("二维码已过期，请重新扫码")
                if platform.system() == "Windows":
                    # 获取pid
                    pid = p.pid

                    # 结束进程
                    os.system("taskkill /F /T /PID %d" % pid)
                else:
                    p.kill()
                flag = login(uid)
                break

        if platform.system() == "Windows":
            # 获取pid
            pid = p.pid

            # 结束进程
            os.system("taskkill /F /T /PID %d" % pid)
        else:
            p.kill()

        return flag

    if not silent_installation:
        flag = login(uid)

        if flag == 0:
            print("登录失败，请重新运行安装程序")
            sys.exit()
        else:
            with open(lagrange_config_path, "r+", encoding="utf-8") as f:
                config = json.load(f)
                config["Account"]["Password"] = password
                f.seek(0)
                json.dump(config, f, ensure_ascii=False, indent=4)
    else:
        with open(lagrange_config_path, "r+", encoding="utf-8") as f:
            config = json.load(f)
            config["Account"]["Password"] = password
            f.seek(0)
            json.dump(config, f, ensure_ascii=False, indent=4)


start_time = time.time()

print("欢迎您使用Lagrange.Onebot安装脚本\n")
print(f"信息确认: \n当前工作目录 {work_path} \n将在 {onebot_path} 安装Lagrange.OneBot\n")

lagrange_path = install()

print("已为您下载最新的Lagrange.Onebot，请坐和放宽\n接下来进入我们需要更改一些配置文件...")
arrangement(lagrange_path)

print(
    f"您本次 Lagrange.Onebot 安装耗时 {int(time.time() - start_time) + 0.114514} 秒，打败全球 19.19810% 的用户\n")
print("青，取之于蓝而青于蓝；冰，水为之而寒于水。\nLagrange.Onebot安装完成，期待与您的下次见面...")
