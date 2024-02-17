# MuRain Bot2(MRB2) 框架文档
**此项目也可称作MuCloud Bot(MCB)框架**
## 首先感谢您选择、使用了MRB2作为您的QQBot框架

### 项目基本目录结构:
```
|- data         MRB2及插件的临时/缓存文件
    |- group
        |- 123  群号为123相关的缓存文件
        ...
    |- json     不属于某个单独群聊的MRB2及插件的josn临时/缓存文件
    ...
|- go-cqhttp    QQBot内核框架，此处以go-cqhttp示例
|- Lib          MRB2的Lib库，插件和MRB2均需要依赖此Lib
    |- MuRainLib.py   MRB2的Lib库之一
    |- QQRichText.py  MRB2的Lib库之一
    |- OnebotAPI.py   MRB2的Lib库之一
|- logs
    |- today.log       当日的日志
    |- xxxx-xx-xx.log  以往的日志
    ...
|- plugins
    |- xxx.py   xxx插件代码
    |- yyy.py   yyy插件代码 
    ...
|- plugin_configs
    |- xxx.yml  xxx插件的配置文件
    |- yyy.yml  yyy插件的配置文件
    ...
|- config.yml   MRB2框架配置文件
|- main.py      MRB2代码（运行这个即可启动）
|- README.md    这个文件就不用解释了吧（？）
```

## 如何部署？
* 下载本项目的releases或源码包
* 若下载的是releases则go-cqhttp已经帮您配置好了正反向HTTP的端口，只需要配置密码即可
* 若下载的是源码包则请自行放入bot框架，并检查端口是否与MRB2配置的一致
* 若下载的是releases则已经帮您把Qsgin服务器也配置好了，只需启动`一键启动.bat`或`一键启动-dev.bat`即可
* 若下载的是源码包请自行启动bot框架
* 随后只需运行MRB2框架即可（main.py）

## MRB2插件编写规范
* 插件名称采用大驼峰命名
* 关于某个单独群聊相关的临时或缓存文件将以json或是数据库的形式存储在`/data/group/<群号>`目录下
* 关于不属于某个单独群聊的临时或缓存文件将以json或是数据库的形式存储在`/data/<存储方式>`目录下
* 临时或缓存文件将以以下方式命名`<插件名称>-<用途>.xx`
* 插件的配置文件将存储在`/plugin_configs`目录下，并以插件名称命名，统一使用yml或yaml当作配置文件
* 在此推荐插件写出详细的log日志，但是如果你硬不写我也没办法（
* 若需要则可引用Lib库，推荐不要重复造轮子，但是如果你硬要我也没办法（
* 需要在插件的头部写上一个类`PluginInfo`，详情请见插件模板（才不是作者懒）
* 为了调用插件则需要创建一个函数`main`，详情请见插件模板（才不是作者懒）
* !!!注意上述所有目录除`/plugins`目录外均有可能未创建，请插件自行检测、创建!!!

## 版权
```
Code with by Xiaosu & Evan. Copyright (c) 2024 GuppyTEAM. All rights reserved.
本代码由校溯 和 XuFuyu编写。版权所有 （c） 2024 Guppy团队。保留所有权利。
```

## 鸣谢
### 在此鸣谢[HarcicYang](https://github.com/HarcicYang)和[kaokao221](https://github.com/kaokao221)为此项目提供了许多的帮助~