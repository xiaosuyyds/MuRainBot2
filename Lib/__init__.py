from Lib.MuRainLib import *
import Lib.EventManager
import Lib.OnebotAPI
import Lib.QQRichText

VERSION = "2.0.0-dev"
VERSION_WEEK = "24Y11A"


# Lib信息
class LibInfo:
    def __init__(self):
        self.version = VERSION
        self.version_week = VERSION_WEEK

    def get_version(self):
        return self.version, self.version_week
