#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|
import logging

BANNER = r""" __  __       ____       _         ____        _   _____ 
|  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
| |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
| |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/ 
|_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|"""
BANNER_LINK = "https://github.com/xiaosuyyds/MuRainBot2"


def color_text(text: str, text_color: tuple[int, int, int] = None, bg_color: tuple[int, int, int] = None):
    text = text + "\033[0m" if text_color is not None or bg_color is not None else text
    if text_color is not None:
        text = f"\033[38;2;{text_color[0]};{text_color[1]};{text_color[2]}m" + text
    if bg_color is not None:
        text = f"\033[48;2;{bg_color[0]};{bg_color[1]};{bg_color[2]}m" + text
    return text


def get_gradient(start_color: tuple[int, int, int], end_color: tuple[int, int, int], length: float):
    # length 为0-1的值，返回一个渐变色当前length的RGB颜色
    return (
        int(start_color[0] + (end_color[0] - start_color[0]) * length),
        int(start_color[1] + (end_color[1] - start_color[1]) * length),
        int(start_color[2] + (end_color[2] - start_color[2]) * length)
    )


# 主函数
if __name__ == '__main__':
    banner_start_color = (14, 190, 255)
    banner_end_color = (255, 66, 179)
    color_banner = ""
    banner = BANNER.split("\n")
    for i in range(len(banner)):
        for j in range(len(banner[i])):
            color_banner += color_text(
                banner[i][j],
                get_gradient(
                    banner_start_color,
                    banner_end_color,
                    ((j / (len(banner[i]) - 1) + i / (len(banner) - 1)) / 2)
                )
            )
        color_banner += "\n"
    print(color_banner + color_text(BANNER_LINK, get_gradient(banner_start_color, banner_end_color, 0.5))
          + color_text("\n正在加载 Lib, 首次启动可能需要几秒钟，请稍等...", banner_start_color), end="")
    import time

    start_loading = time.time()

    from Lib import *
    Logger.init()

    from Lib.core import *

    Logger.set_logger_level(logging.DEBUG if ConfigManager.GlobalConfig().debug.enable else logging.INFO)

    print("\r" + color_text(
        f"Lib 加载完成！耗时: {round(time.time() - start_loading, 2)}s 正在启动 MuRainBot...",
        banner_end_color
    )
          )

    logger = Logger.get_logger()
    logger.info("日志初始化完成！")

    logger.info("启动监听服务器")
    ListenerServer.server.serve_forever()
