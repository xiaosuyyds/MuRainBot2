<h1 align="center">MuRain Bot2(MRB2)</h1>
<p align="center" class="shields">
    <a href="https://github.com/xiaosuyyds/MuRainBot2/issues" style="text-decoration:none">
        <img src="https://img.shields.io/github/issues/xiaosuyyds/MuRainBot2.svg?style=for-the-badge" alt="GitHub issues"/>
    </a>
    <a href="https://github.com/xiaosuyyds/MuRainBot2/stargazers" style="text-decoration:none" >
        <img src="https://img.shields.io/github/stars/xiaosuyyds/MuRainBot2.svg?style=for-the-badge" alt="GitHub stars"/>
    </a>
    <a href="https://github.com/xiaosuyyds/MuRainBot2/forks" style="text-decoration:none" >
        <img src="https://img.shields.io/github/forks/xiaosuyyds/MuRainBot2.svg?style=for-the-badge" alt="GitHub forks"/>
    </a>
    <!--
    <a href="https://github.com/xiaosuyyds/MuRainBot2/actions">
        <img src="https://img.shields.io/github/actions/workflow/status/xiaosuyyds/MuRainBot2/vuepress-deploy.yml?style=for-the-badge">
    </a>
    -->
    <a href="https://github.com/xiaosuyyds/MuRainBot2/blob/master/LICENSE" style="text-decoration:none" >
        <img src="https://img.shields.io/static/v1?label=LICENSE&message=GPL-3.0&color=lightrey&style=for-the-badge" alt="GitHub license"/>
    </a>
    <a href="https://github.com/botuniverse/onebot" style="text-decoration:none">
        <img src="https://img.shields.io/badge/OneBot-11-black?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHAAAABwCAMAAADxPgR5AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAAxQTFRF////29vbr6+vAAAAk1hCcwAAAAR0Uk5T////AEAqqfQAAAKcSURBVHja7NrbctswDATQXfD//zlpO7FlmwAWIOnOtNaTM5JwDMa8E+PNFz7g3waJ24fviyDPgfhz8fHP39cBcBL9KoJbQUxjA2iYqHL3FAnvzhL4GtVNUcoSZe6eSHizBcK5LL7dBr2AUZlev1ARRHCljzRALIEog6H3U6bCIyqIZdAT0eBuJYaGiJaHSjmkYIZd+qSGWAQnIaz2OArVnX6vrItQvbhZJtVGB5qX9wKqCMkb9W7aexfCO/rwQRBzsDIsYx4AOz0nhAtWu7bqkEQBO0Pr+Ftjt5fFCUEbm0Sbgdu8WSgJ5NgH2iu46R/o1UcBXJsFusWF/QUaz3RwJMEgngfaGGdSxJkE/Yg4lOBryBiMwvAhZrVMUUvwqU7F05b5WLaUIN4M4hRocQQRnEedgsn7TZB3UCpRrIJwQfqvGwsg18EnI2uSVNC8t+0QmMXogvbPg/xk+Mnw/6kW/rraUlvqgmFreAA09xW5t0AFlHrQZ3CsgvZm0FbHNKyBmheBKIF2cCA8A600aHPmFtRB1XvMsJAiza7LpPog0UJwccKdzw8rdf8MyN2ePYF896LC5hTzdZqxb6VNXInaupARLDNBWgI8spq4T0Qb5H4vWfPmHo8OyB1ito+AysNNz0oglj1U955sjUN9d41LnrX2D/u7eRwxyOaOpfyevCWbTgDEoilsOnu7zsKhjRCsnD/QzhdkYLBLXjiK4f3UWmcx2M7PO21CKVTH84638NTplt6JIQH0ZwCNuiWAfvuLhdrcOYPVO9eW3A67l7hZtgaY9GZo9AFc6cryjoeFBIWeU+npnk/nLE0OxCHL1eQsc1IciehjpJv5mqCsjeopaH6r15/MrxNnVhu7tmcslay2gO2Z1QfcfX0JMACG41/u0RrI9QAAAABJRU5ErkJggg==" alt="Badge">
    </a>
    <br>
    <a href="https://github.com/xiaosuyyds/MuRainBot2">
        <img src="https://counter.seku.su/cmoe?name=murainbot2&theme=rule34" alt=""/>
    </a>
</p>

| 简体中文 | [English](README_EN.md) |

### 这是一个基于python适配onebot11协议的QQBot ~~(框架?)~~
### 首先感谢您选择/使用了MRB2作为您的QQBot
##### ~~作者自己写着用的，有一些写的不好的地方还请见谅（不过估计也没人会用我这个项目吧）~~
~~*此项目也可称作MuCloud Bot(MCB)*~~

~~*什么？你问我为什么要叫MRB2，因为这个框架是给我的一个叫做沐雨的qqbot写的，然后之前还有[一个写的很垃圾](https://github.com/xiaosuyyds/PyQQbot)的版本，所以就叫做MRB2*~~



<details>
<summary>查看基本看目录结构</summary>

```
├─ data         MRB2及插件的临时/缓存文件
│   ├─ group  每个群的相关的缓存文件
│   │   ├─ 123  群号为123相关的缓存文件（示例）
│   │   ...
│   ├─ json     不属于某个单独群聊的MRB2及插件的json临时/缓存文件
│   ...
├─ Lagrange.Core    QQBot内核框架，此处以Lagrange.Core示例
├─ Lib          MRB2的Lib库，插件和MRB2均需要依赖此Lib
│   ├─ __init__.py     MRB2Lib
│   ├─ BotController.py   MRB2的Lib库之一，用于控制Bot
|   ├─ Configs.py      MRB2的Lib库之一，用于配置文件的一些功能
│   ├─ EventManager.py MRB2的Lib库之一，用于广播上报事件
│   ├─ FileCacher.py   MRB2的Lib库之一，用于缓存、读取文件
│   ├─ Logger.py       MRB2的Lib库之一，用于记录日志
│   ├─ MuRainLib.py    MRB2的Lib库之一，用于提供一些零七八碎的函数
│   ├─ OnebotAPI.py    MRB2的Lib库之一，用于调用OneBotAPI
│   ├─ QQRichText.py   MRB2的Lib库之一，用于解析/处理QQ消息
│   ├─ ThreadPool.py   MRB2的Lib库之一，用于多线程（线程池）处理
│   ...
├─ logs
│   ├─ latest.log       当日的日志
│   ├─ xxxx-xx-xx.log  以往的日志
│   ...
├─ plugins
│   ├─ xxx.py   xxx插件代码
│   ├─ yyy.py   yyy插件代码 
│   ...
├─ plugin_configs
│   ├─ pluginTemplates.py  插件模板
│   ├─ xxx.yml  xxx插件的配置文件
│   ├─ yyy.yml  yyy插件的配置文件
│   ...
├─ config.yml   MRB2配置文件
├─ main.py      MRB2代码（运行这个即可启动）
├─ README.md    这个文件就不用解释了吧（？）
└─ README_en.md No need to explain this file, right?
```

</details>


## 💻如何部署？
**作者在python3.10编写、测试均未发现问题，其他版本暂未测试**

### 可查看本项目的[`文档`](docs/readme.md) 

[//]: # (* 下载本项目的releases或源码包)

[//]: # (* 请下载python环境，并使用pip安装[`requirements.txt`]&#40;requirements.txt&#41;内的库)

[//]: # (* [**installer.py**]&#40;installer.py&#41;)

[//]: # (  * 运行[`installer.py`]&#40;installer.py&#41;随后静待安装成功)

[//]: # (  * 配置好之后运行先运行`Lagrange.OneBot`然后运行`main.py`即可)

[//]: # (* ~~**releases**~~)

[//]: # (  * 首先配置Lagrange.OneBot的`appsettings.json`，如有需要可以修改正反向HTTP端口)

[//]: # (  * 随后配置一下MRB2的[`config.yml`]&#40;config.yml&#41;账号和QQ号)

[//]: # (  * 配置好之后运行先运行`Lagrange.OneBot`然后运行`main.py`即可)

[//]: # (* ~~**源码包**~~)

[//]: # (  * 自行配置框架，并修改正反向HTTP端口，与框架匹配)

[//]: # (  * 随后配置一下MRB2的[`config.yml`]&#40;config.yml&#41;账号和QQ号)

[//]: # (  * 配置好之后运行先运行框架然后运行`main.py`即可)

## 📕关于版本
* 目前MRB2版本为2.0.0-dev

~~*你问我为什么第一个版本就是2.0.0?因为这是MRB2嘛自然就是2.0.0开始的咯*~~
* 关于版本号与版本周的说明：
   * 版本号格式为`<主版本>.<次版本>.<修订版本>-<特殊提醒/版本(如果有)>` 例如`2.0.0`
   * 测试版版本号后统一添加`-dev`后缀 例如`2.0.0-dev`
   * 测试版本的版本周格式为`<年份>W<周数><当周内更新的版本数A-Z排列>` 例如`29W10A`
   * 正式版本的版本周格式为`<年份>Y<周数>W` 例如`24Y09W`

## 🧩插件
> _~~插件是MRB2的灵魂，没有插件的MRB2只是一个空壳~~_
### MRB2本身不具备任何实际上的功能，一切都需要编写插件来实现功能
### MRB2插件编写规范

* 插件名称采用大驼峰命名
* 关于某个单独群聊相关的临时或缓存文件将以json或是数据库的形式存储在`/data/group/<群号>`目录下
* 关于不属于某个单独群聊的临时或缓存文件将以json或是数据库的形式存储在`/data/<存储方式>`目录下
* 临时或缓存文件将以以下方式命名`<插件名称>-<用途>.xx`，并存放在`/data/cache`目录下
* 插件的配置文件将存储在`/plugin_configs`目录下，并以插件名称命名，统一使用yml或yaml当作配置文件
* 在此推荐插件写出详细的log日志，但是如果你硬不写我也没办法（
* 若需要则可引用Lib库，推荐不要重复造轮子，但是如果你硬要我也没办法（
* 需要在插件的头部写上一个类`PluginInfo`，详情请见[插件模板](plugins/pluginTemplates.py) ~~（才不是作者懒）~~
* 为了调用插件可以创建一个函数`main`，详情请见[插件模板](plugins/pluginTemplates.py) ~~（才不是作者懒，好吧我就是懒）~~
* 如果没有函数`main`则需要在初始化的时候自行注册各个事件响应的函数。
* ***!!!注意上述所有目录除`/plugins`目录外均有可能未创建，请插件自行检测、创建!!!***
* 插件的代码请放在`/plugins`目录下，以插件名称命名，统一使用`py`或`pyc`作为文件后缀

#### 不过我们有一些我们自己制作的插件，后续可能会放在源码中或是releases中

## ❤️鸣谢❤️

### 请勿直接提交到[`master`](https://github.com/xiaosuyyds/MuRainBot2)分支，请先提交到[`dev`](https://github.com/xiaosuyyds/MuRainBot2/tree/dev)分支，随后再创建PR合并分支
### 感谢所有为此项目做出贡献的大大，你们的存在，让社区变得更加美好~！
<a href="https://github.com/xiaosuyyds/MuRainBot2/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=xiaosuyyds/MuRainBot2&max=999" alt=感谢他们（鼓掌）！>
</a>

### 以及特别鸣谢[HarcicYang](https://github.com/HarcicYang)和[kaokao221](https://github.com/kaokao221)为此项目提供了许多的帮助~


## ⭐StarHistory⭐

[![](https://api.star-history.com/svg?repos=xiaosuyyds/MuRainBot2&type=Date)](https://github.com/xiaosuyyds/MuRainBot2/stargazers)
