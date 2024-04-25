# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

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


VERSION = "2.0.0-dev"
VERSION_WEEK = "24W13A"


# Lib信息
class LibInfo:
    def __init__(self):
        self.version = VERSION
        self.version_week = VERSION_WEEK

    def get_version(self):
        return self.version, self.version_week
