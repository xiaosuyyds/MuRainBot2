<h1 align="center">MuRain Bot2(MRB2)</h1>
<p align="center" class="shields">
    <a href="https://github.com/xiaosuyyds/MuRainBot2/issues" style="text-decoration:none">
        <img src="https://img.shields.io/github/issues/xiaosuyyds/MuRainBot2.svg?style=for-the-badge" alt="GitHub issues"/>
    </a>
    <a href="https://github.com/xiaosuyyds/MuRainBot2/stargazers" style="text-decoration:none" >
        <img src="https://img.shields.io/github/stars/xiaosuyyds/MuRainBot2.svg?style=for-the-badge" alt="GitHub stars"/>
    </a>
    <a href="https://github.com/xiaosuyyds/MuRainBot2/network" style="text-decoration:none" >
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

| [简体中文](README.md) | English |

### This is a QQBot (framework?) based on python adapted to the onebot11 protocol.
### First of all, thank you for choosing/using MRB2 as your QQ Bot
~~*This project can also be called MuCloudBot(MCB)*~~

<details>
<summary>Check the basic directory structure</summary>

```
├─ data         Temporary/cached files for MRB2 and plug-ins
│   ├─ group    The relevant cache files for each cluster
│   │   ├─ 123  Cache files related to GroupID 123 (example)
│   │   ...
│   ├─ json     MRB2 and the json temporary/cached files of the plugin that do not belong to a separate group chat
│   ...
├─ go-cqhttp    QQBot core framework, here exemplified by go-cqhttp
├─ Lib          MRB2's Lib library, plugins and MRB2 both depend on this Lib
│   ├─ __init__.py     MRB2Lib
│   ├─ BotController.py   One of MRB2's Lib libraries, used to control the Bot
|   ├─ Configs.py      One of MRB2's Lib libraries, used for some configuration file functions
│   ├─ EventManager.py One of MRB2's Lib libraries, used to broadcast reported events
│   ├─ FileCacher.py   One of MRB2's Lib libraries, used for caching, reading files
│   ├─ Logger.py       One of MRB2's Lib libraries, used for logging
│   ├─ MuRainLib.py    One of MRB2's Lib libraries, used to provide some miscellaneous functions
│   ├─ OnebotAPI.py    One of MRB2's Lib libraries, used to call OneBotAPI
│   ├─ QQRichText.py   One of MRB2's Lib libraries, used for parsing/handling QQ messages
│   ├─ ThreadPool.py   One of MRB2's Lib libraries, used for multithreading (thread pool) processing
│   ...
├─ logs
│   ├─ latest.log       Today's log
│   ├─ xxxx-xx-xx.log  Past logs
│   ...
├─ plugins
│   ├─ xxx.py   xxx plugin code
│   ├─ yyy.py   yyy plugin code 
│   ...
├─ plugin_configs
│   ├─ pluginTemplates.py  Plugin template
│   ├─ xxx.yml  Configuration file for xxx plugin
│   ├─ yyy.yml  Configuration file for yyy plugin
│   ...
├─ config.yml   MRB2 configuration file
├─ main.py      MRB2 code (run this to start)
├─ README.md    这个文件就不用解释了吧（？）
└─ README_en.md No need to explain this file, right?
```

</details>

## 💻How To Deploy?
**The author has written and tested in python3.10 without any problems, other versions have not been tested yet**
* Download the releases or source code package of this project
* Please download the python environment and use pip to install the libraries in [`requirements.txt`](requirements.txt)
* **Releases**
    * First, configure the account and password in go-cqhttp's `config.yml`, if necessary, you can modify the HTTP ports
    * Then configure MRB2's [`config.yml`](config.yml) account and QQ number
    * After configuring, run `go-cqhttp` and `Qsgin` server first, then run `main.py`
* **Source code package**
    * Configure the framework yourself, and modify the HTTP ports to match the framework
    * Then configure MRB2's [`config.yml`](config.yml) account and QQ number
    * After configuring, run the framework first, then run `main.py`

## 📕About The Version
* The current version of MRB2 is 2.0.0-dev
* Explanation of version number and version week:
    * The version number format is `<major version>.<minor version>.<patch version>-<special reminder/version (if any)>` e.g., `2.0.0`
    * Test versions uniformly add the `-dev` suffix to the version number, e.g., `2.0.0-dev`
    * The version week format for test versions is `<year>W<week number><version number within the week A-Z>` e.g., `29W10A`
    * The version week format for official versions is `<year>Y<week number>W` e.g., `24Y09W`

## 🧩Plugins
> _~~Plugins are the soul of MRB2, and MRB2 without plugins is just an empty shell~~_

#### **MRB2 itself does not have any actual functionality, everything needs to be implemented by writing plugins**
### MRB2 plugin writing specifications
  * Plugin names use CamelCase
  * Temporary or cached files related to a specific group chat will be stored in `/data/group/<group number>` directory in json or database format
  * Temporary or cached files not related to a specific group chat will be stored in `/data/<storage method>` directory in json or database format
  * Temporary or cached files will be named in the following way `<plugin name>-<purpose>.xx`
  * The plugin's configuration files will be stored in the `/plugin_configs` directory, named after the plugin, uniformly using yml or yaml as the configuration file
  * It is recommended to write detailed log logs for the plugin, but if you don't write it, I can't do anything about it
  * If needed, you can reference the Lib library, it is recommended not to reinvent the wheel, but if you insist, I can't do anything about it
  * You need to write a class `PluginInfo` at the top of the plugin, for details, please see [plugin template](plugins/pluginTemplates.py) ~~(it's not that the author is lazy)~~
  * To call the plugin, you can create a function `main`, for details, please see [plugin template](plugins/pluginTemplates.py) ~~(it's not that the author is lazy, okay, I am lazy)~~
  * If there is no `main` function, you need to register the functions that respond to various events during initialization.
  * ***!!!Note that all directories except the `/plugins` directory may not have been created, please check and create them yourself!!!***
  * Please put the plugin code in the `/plugins` directory, named after the plugin, uniformly using `py` or `pyc` as the file extension

#### However, we have some plugins that we made ourselves, which may be included in the source code or releases later

## ❤️Acknowledgements❤️

### Please do not submit directly to the [`master`](https://github.com/xiaosuyyds/MuRainBot2) branch, please submit to the [`dev`](https://github.com/xiaosuyyds/MuRainBot2/tree/dev) branch first, then create a PR to merge branches
### Thanks to all the contributors to this project, your existence makes the community a better place~!
![Thanks to them (applause)!](https://contrib.rocks/image?repo=xiaosuyyds/MuRainBot2&max=999)

### And special thanks to [HarcicYang](https://github.com/HarcicYang) and [kaokao221](https://bing.com/search?q=)

## ⭐StarHistory⭐

![Star History](https://api.star-history.com/svg?repos=xiaosuyyds/MuRainBot2&type=Date)