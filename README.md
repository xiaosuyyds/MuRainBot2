# <div style="text-align: center;"> MuRain Bot2(MRB2)
<div style="text-align: center;">
   <p class="shields">
       <a href="https://github.com/xiaosuyyds/MuRainBot2/issues" style="text-decoration:none">
           <img src="https://img.shields.io/github/issues/xiaosuyyds/MuRainBot2.svg" alt="GitHub issues"/>
       </a>
       <a href="https://github.com/xiaosuyyds/MuRainBot2/stargazers" style="text-decoration:none" >
           <img src="https://img.shields.io/github/stars/xiaosuyyds/MuRainBot2.svg" alt="GitHub stars"/>
       </a>
       <a href="https://github.com/xiaosuyyds/MuRainBot2/network" style="text-decoration:none" >
           <img src="https://img.shields.io/github/forks/xiaosuyyds/MuRainBot2.svg" alt="GitHub forks"/>
       </a>
       <!--
       <a href="https://github.com/xiaosuyyds/MuRainBot2/actions">
           <img src="https://img.shields.io/github/actions/workflow/status/xiaosuyyds/MuRainBot2/vuepress-deploy.yml">
       </a>
       -->
       <a href="https://github.com/xiaosuyyds/MuRainBot2/blob/master/LICENSE" style="text-decoration:none" >
           <img src="https://img.shields.io/static/v1?label=LICENSE&message=GPL-3.0&color=lightrey" alt="GitHub license"/>
       </a>
   </p>
</div>

### 这是一个基于python 适配onebot11协议的QQBot ~~(框架?)~~
### 首先感谢您选择/使用了MRB2作为您的QQBot
~~*此项目也可称作MuCloud Bot(MCB)*~~



<details>
<summary><B><span style="font-size: x-large; ">查基本看目录结构</span></B></summary>

```
├─ data         MRB2及插件的临时/缓存文件
│   ├─ group
│   │   ├─ 123  群号为123相关的缓存文件
│   │   ...
│   ├─ json     不属于某个单独群聊的MRB2及插件的json临时/缓存文件
│   ...
├─ go-cqhttp    QQBot内核框架，此处以go-cqhttp示例
├─ Lib          MRB2的Lib库，插件和MRB2均需要依赖此Lib
│   ├─ MuRainLib.py   MRB2的Lib库之一
│   ├─ QQRichText.py  MRB2的Lib库之一
│   ├─ OnebotAPI.py   MRB2的Lib库之一
├─ logs
│   ├─ today.log       当日的日志
│   ├─ xxxx-xx-xx.log  以往的日志
│   ...
├─ plugins
│   ├─ xxx.py   xxx插件代码
│   ├─ yyy.py   yyy插件代码 
│   ...
├─ plugin_configs
│   ├─ xxx.yml  xxx插件的配置文件
│   ├─ yyy.yml  yyy插件的配置文件
│   ...
├─ config.yml   MRB2配置文件
├─ main.py      MRB2代码（运行这个即可启动）
└─ README.md    这个文件就不用解释了吧（？）
```

</details>


## 如何部署？
* 下载本项目的releases或源码包
* 若下载的是releases则go-cqhttp已经帮您配置好了正反向HTTP的端口，只需要配置密码即可
* 若下载的是源码包则请自行放入bot框架，并检查端口是否与MRB2配置的一致
* 若下载的是releases则已经帮您把Qsgin服务器也配置好了
* 若下载的是源码包请自行启动bot框架
* 随后只需运行MRB2即可（main.py）

## 关于版本
 * 目前MRB2版本为2.0.0-dev
 * 关于版本号与版本周的说明：
    * 版本号格式为`<主版本>.<次版本>.<修订版本>-<特殊提醒/版本(如果有)>` 例如`2.0.0`
    * 测试版版本号后统一添加`-dev`后缀 例如`2.0.0`
    * 测试版本的版本周格式为`<年份>W<周数><当周内更新的版本数A-Z排列>` 例如`29W10A`
    * 正式版本的版本周格式为`<年份>Y<周数>W` 例如`24Y09W`

## 插件
### MRB2本身不具备任何实际上的功能，一切都需要编写插件来实现功能
### MRB2插件编写规范

* 插件名称采用大驼峰命名
* 关于某个单独群聊相关的临时或缓存文件将以json或是数据库的形式存储在`/data/group/<群号>`目录下
* 关于不属于某个单独群聊的临时或缓存文件将以json或是数据库的形式存储在`/data/<存储方式>`目录下
* 临时或缓存文件将以以下方式命名`<插件名称>-<用途>.xx`
* 插件的配置文件将存储在`/plugin_configs`目录下，并以插件名称命名，统一使用yml或yaml当作配置文件
* 在此推荐插件写出详细的log日志，但是如果你硬不写我也没办法（
* 若需要则可引用Lib库，推荐不要重复造轮子，但是如果你硬要我也没办法（
* 需要在插件的头部写上一个类`PluginInfo`，详情请见插件模板 ~~（才不是作者懒）~~
* 为了调用插件则需要创建一个函数`main`，详情请见插件模板 ~~（才不是作者懒，好吧我就是懒）~~
* !!!注意上述所有目录除`/plugins`目录外均有可能未创建，请插件自行检测、创建!!!

#### 不过我们有一些我们自己制作的插件，后续可能会放在源码中或是releases中

## 鸣谢

### 感谢所有为此项目做出贡献的大大~你们的存在，让社区变得更加美好~！
<a href="https://github.com/xiaosuyyds/MuRainBot2/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=xiaosuyyds/MuRainBot2&max=999" alt=感谢他们（鼓掌）！>
</a>

### 以及特别鸣谢[HarcicYang](https://github.com/HarcicYang)和[kaokao221](https://github.com/kaokao221)为此项目提供了许多的帮助~
