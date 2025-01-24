#   __  __       ____       _         ____        _
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __|
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|

from Lib import *
from Lib.core import PluginManager, ConfigManager

logger = Logger.get_logger()

plugin_info = PluginManager.PluginInfo(
    NAME="Helper",
    AUTHOR="Xiaosu",
    VERSION="1.0.0",
    DESCRIPTION="用于获取插件帮助信息",
    HELP_MSG="发送 /help 或 /帮助 以获取所有插件的帮助信息"
)


@common.function_cache(1)
def get_help_text():
    plugins = PluginManager.plugins
    text = f"{ConfigManager.GlobalConfig().account.nick_name} 帮助"
    for plugin in plugins:
        try:
            plugin_info = plugin["info"]
            if plugin_info.DESCRIPTION and plugin_info.IS_HIDDEN is False:
                text += f"\n{plugin_info.NAME} - {plugin_info.DESCRIPTION}"
        except Exception as e:
            logger.warning(f"获取插件{plugin['name']}信息时发生错误: {repr(e)}")
    text += "\n----------\n发送/help <插件名>或/帮助 <插件名>以获取插件详细帮助信息"
    return text


rule = EventHandlers.CommandRule("help", aliases={"帮助"})

matcher = EventHandlers.on_event(EventClassifier.GroupMessageEvent, priority=0, rules=[rule])


@matcher.register_handler()
def on_help(event_data):
    if event_data.message == "帮助" or event_data.message == "help":
        Actions.SendMsg(
            message=QQRichText.QQRichText(
                QQRichText.Reply(event_data["message_id"]),
                get_help_text()
            ), group_id=event_data["group_id"]
        ).call()
    else:
        plugin_name = str(event_data.message).split(" ", 1)[1].lower()
        for plugin in PluginManager.plugins:
            try:
                plugin_info = plugin["info"]
                if plugin_info.NAME.lower() == plugin_name and plugin_info.IS_HIDDEN is False:
                    Actions.SendMsg(
                        message=QQRichText.QQRichText(
                            QQRichText.Reply(event_data["message_id"]),
                            plugin_info.HELP_MSG + "\n----------\n发送/help以获取全部的插件帮助信息"
                        ), group_id=event_data["group_id"]
                    ).call()
                    return
            except:
                pass
        else:
            Actions.SendMsg(
                message=QQRichText.QQRichText(
                    QQRichText.Reply(event_data["message_id"]),
                    "没有找到此插件，请检查是否有拼写错误"
                ), group_id=event_data["group_id"]
            ).call()
