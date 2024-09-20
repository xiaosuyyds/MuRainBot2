# 欢迎来到MuRainBot2的文档！
> 本文档可能并非适用于最新的代码，如遇到错误可以发送issue给我，我会尽快回复的！
### 在这里，你将会学会：
 - 如何部署这个项目
 - 如何使用这个项目
 - 如何自己写一个插件
 - 这个项目的SDK该如何使用

## 快速开始
> 首先我们需要部署下载这个项目
1. 打开本项目的主页~
2. 点击“Code”按钮
3. 点击“Download ZIP”
> 什么？你说你找不到？这是链接，直接戳这个下载吧: [我是链接](https://github.com/xiaosuyyds/MuRainBot2/archive/refs/heads/master.zip)
---
> 很好，我相信你已经成功下载了这个项目，接下来开始配置~
1. 打开下载的压缩包，解压
2. 安装 [Python](https://www.python.org/downloads/)\
~~什么？你说你不会装Python？那我建议你别用我这项目了~~
3. 在终端运行 `python -m pip install -r requirements.txt`\
~~什么？你问我这个命令是干嘛的？它啊其实是用来安装本项目运行必须的依赖库的哦~~\
~~什么？你又问这个命令为什么运行不了？请检查你是否已经安装好了Python，以及你是否正确设置了环境变量，以及你是否已经将cmd/PowerShell切换到项目文件夹下~~
4. 运行 `python main.py`
> 很棒，你肯定已经成功运行了，那么此时你应该在终端内发现了几条log和一个ERROR提示，不要担心，这是正常情况，接下来我们来解决它~
**附：正常启动的log**
```text
[2024-09-18 11:32:12] [main.py] [INFO]: MuRain Bot开始运行，当前版本：2.0.0-dev(24W18A)
[2024-09-18 11:32:12] [main.py] [INFO]: MuRainLib版本校验成功！
[2024-09-18 11:32:12] [main.py] [INFO]: MuRainLib当前版本：2.0.0-dev(24W18A)
[2024-09-18 11:32:12] [main.py] [INFO]: 插件导入完成，共成功导入 2 个插件:
[2024-09-18 11:32:12] [main.py] [INFO]:  - Helper: Helper 作者:校溯
[2024-09-18 11:32:12] [main.py] [INFO]:  - pluginTemplates: HelloWorld 作者:You
[2024-09-18 11:32:12] [main.py] [INFO]: 读取到监听服务器ip，将以此ip启动监听服务器: 127.0.0.1:5701
[2024-09-18 11:32:12] [main.py] [INFO]: 读取到监听api，将以此url调用API: http://127.0.0.1:5700
[2024-09-18 11:32:12] [main.py] [WARNING]: 配置文件中未找到BotUID或昵称，将自动获取！
[2024-09-18 11:32:14] [main.py] [ERROR]: 获取BotUID与昵称失败！可能会导致严重问题！报错信息：ConnectionError(MaxRetryError("HTTPConnectionPool(host='127.0.0.1', port=5700): Max retries exceeded with url: /get_login_info (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x0000023299760490>: Failed to establish a new connection: [WinError 10061] 由于目标计算机积极拒绝，无法连接。'))"))
[2024-09-18 11:32:14] [main.py] [INFO]: 欢迎使用 (123456)
[2024-09-18 11:32:14] [main.py] [INFO]: 开启命令输入
[2024-09-18 11:32:14] [main.py] [INFO]: 启动监听服务器
```
---
### 安装Onebot实现端
> 什么，你问我什么是Onebot？它是一个QQ机器人协议，额……忘词了，[你自己看吧](https://github.com/botuniverse/onebot-11/)

#### 那么，我们如何安装Onebot实现端？首先你要知道市面上的Onebot实现端有很多，目前主流的有:
- [Lagrange.Onebot](https://github.com/LagrangeDev/Lagrange.Core)
- [OpenShamrock](https://github.com/whitechi73/OpenShamrock)
- [LLOneBot](https://github.com/LLOneBot/LLOneBot)
- [NapCat](https://github.com/NapNeko/NapCatQQ)
- [~~go-cqhttp~~](https://github.com/Mrs4s/go-cqhttp)
#### 以上这些项目基本上均有详细的安装文档，请自行查看，在此我们使用Lagrange.Onebot进行示范(~~才不是我懒~~)
有两种方法，1.使用作者写的小工具全自动安装，2.手动安装
> 使用作者写的小工具自动安装

首先打开作者写的小工具的项目[Lagrange.Installer](https://github.com/xiaosuyyds/Lagrange.Installer)

然后下载[releases](https://github.com/xiaosuyyds/Lagrange.Installer/releases)内的最新版本

随后将下载的exe拖到你下载本项目的目录下，然后运行，跟随提示，完成下载及首次登陆流程

> 手动安装

我懒得写了，自己看[Lagrange.Onebot](https://github.com/LagrangeDev/Lagrange.Core)的[文档](https://lagrangedev.github.io/Lagrange.Doc/)吧

然后把Lagrange.Onebot的配置文件(`appsettings.json`)中的`Implementations`字段修改为以下内容:
```json
"Implementations": [
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
```
---
> 恭喜你，你已经成功安装Onebot实现端，接下来我们开始配置MuRainBot2吧！

首先打开MuRainBot2的配置文件(`config.yml`)

让我来为您一一介绍……还是算了，`config.yml`有完善的注释，相信你看得懂！

您只需要在account.bot_admin中添加您自己的QQ号即可，其余的配置项暂时可以不用管他

---

> 接下来就是最后一步，运行MuRainBot2和Onebot实现了了！

Onebot实现端你自己启动吧，我懒得写了，文档都有的

MuRainBot2运行命令为`python main.py`

### 至此，您已经成功安装并配置了MuRainBot2，请尽情享用吧！

> 更进一步: 了解如何自行编写插件

~~这部分还没写完，如果有实力的可以提个pr帮我写（~~