# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

import os
# 修改工作目录
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Lib.MuRainLib import *
import Lib.OnebotAPI as OnebotAPI
import Lib.QQRichText as QQRichText
import Lib.EventManager as EventManager
import Lib.Logger as Logger
import Lib.BotController as BotController
import Lib.Configs as Configs
import Lib.FileCacher as FileCacher
import Lib.ThreadPool as ThreadPool
import Lib.ListeningServer as ListeningServer
import Lib.PluginManager as PluginManager
import Lib.QQDataCacher as QQDataCacher
import Lib.Command as Command

# 扩展模块
import Lib.Extra as Extra

VERSION = "2.0.0-dev"
VERSION_WEEK = "24W18A"


# Lib信息
class LibInfo:
    main_version, main_version_week = None, None

    def __init__(self):
        self.version = VERSION
        self.version_week = VERSION_WEEK

    def get_lib_version(self):
        return self.version, self.version_week

    def get_main_version(self):
        return self.main_version, self.main_version_week

