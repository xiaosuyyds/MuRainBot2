# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|

"""
OnebotAPI
可以方便的调用Onebot的API
"""
import requests
import urllib.parse


# TODO: API调用模板（给每个API写个class方便调用）
class OnebotAPI:
    def __init__(self, host: str = "", port: int = -1, original: bool = False):
        """
        :param host: 调用的ip
        :param port: 调用的端口
        :param original: 是否返回全部json（默认只返回data内）
        """
        # if url != "":
        #     url_list = urllib.parse.urlparse(url)
        #     host = url_list.scheme + "//" + url_list.netloc
        #     port = url_list.port
        #     node = url_list.path
        # else:
        #     node = ""
        self.host = host
        self.port = port
        self.node = ""
        self.data = None
        self.original = original

    def __str__(self):
        if not (self.host.startswith("http://") or self.host.startswith("https://")):
            self.host = "http://" + self.host
        # 拼接url
        self.url = urllib.parse.urljoin(self.host + ":" + str(self.port), self.node)
        return self.url

    def set_node(self, node: str, data: dict = None):
        if data is None:
            data = {}
        self.node = node
        self.data = data
        return str(self)

    def set_ip(self, host: str, port: int):
        self.host = host
        self.port = port

    def get(self, node: str = "", data: dict = None):
        if node != "":
            self.node = node
        if data is not None:
            self.data = data

        self.node = node
        self.data = data

        if self.node == "":
            # raise ValueError('The node cannot be empty.')
            self.node = "/"

        if self.host == "":
            raise ValueError('The host cannot be empty.')

        if self.port == -1:
            raise ValueError('The port cannot be empty.')

        # 发起get请求
        try:
            response = requests.get(str(self), params=self.data)
            # 获取返回值
            result = response.json()['data']
            # 如果original为真，则返回原值和response
            if self.original:
                return result, response
            else:
                return result
        except Exception as e:
            # 返回异常信息
            return e
