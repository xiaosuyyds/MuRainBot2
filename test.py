from Lib import MuRainLib
from Lib import OnebotAPI
from Lib import QQRichText

main = MuRainLib.LibInfo()

# log = MuRainLib.log_init()


# class plugins_information:
#     def __init__(self):
#         self.NAME = "AIChat-2"  # 插件名称
#         self.AUTHOR = "校溯"  # 插件作者
#         self.VERSION = "1.0"  # 插件版本
#         self.DESCRIPTION = "AI聊天插件"  # 插件描述
#         self.HELP_MSG = ""  # 插件帮助
#         self.OFFICIAL_WEBSITE = "木有"  # 插件官网


# print(main.version)

# print()

cq = QQRichText.QQRichText(rich_text="[CQ:at,qq=%s] 我吃柠檬" % 123)
print(cq)
print(cq.get())


api = OnebotAPI.OnebotAPI(host="0.0.0.0", port=576)
print(api.set_node(node="114514", data={"114514": 1919810}))
print(api)
print(api.get())
# logging.info('test运行结束！')
