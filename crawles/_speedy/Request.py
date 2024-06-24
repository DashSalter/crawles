from copy import copy
from typing import Literal
from .api import post, get
from objprint import add_objprint


class Retry:
    def __init__(self):
        self.retry_request = False  # 是否重试请求
        self.retry_total: int = 3  # 最大重试次数
        self.retry_interval = 1  # 重试间隔/秒


@add_objprint
class Request:  # 请求对象类
    def __init__(self):
        self.url = None  # 网址
        self.cookies: dict = {}  # cookie
        self.headers: dict = {}  # 请求头
        self.data: dict = {}  # 请求体
        self.proxies = None  # 代理
        self.callback = None  # 回调函数
        self.__method: str = 'GET'  # 请求方法 method
        self.index: int = 0  # 请求索引

        self.info: str = ''  # 输出提示信息
        self.timeout: (None, int, float) = None  # 请求等待时间
        self.retry = Retry()  # 请求重试
        self.request_sleep: (int, float) = 0  # 请求间隔
        self.random_user_agent: bool = False  # 随机请求头

        self.current_retry = 0  # 当前请求次数

    def pre_request_callback(self, request) -> None:
        """预请求回调"""
        if not self.random_user_agent:
            return  # 是否使用随机请求头
        from random import choice
        from .user_agent import USER_AGENT_LIST
        request.headers['User-Agent'] = choice(USER_AGENT_LIST)

    def make_request(self):
        """发起请求"""
        response_ = self.method_map(**self.options())
        return response_

    @property
    def method_map(self) -> (post, get):
        """请求映射"""
        return post if self.__method in ['POST', 'JSON_POST'] else get

    def options(self) -> dict:
        """请求参数封装"""
        common_options: dict = {'url': self.url, 'cookies': self.cookies, 'headers': self.headers,
                                'proxies': self.proxies, 'timeout': self.timeout}
        if self.__method == 'GET':
            common_options['params'] = self.data
        elif self.__method == 'POST':
            common_options['data'] = self.data
        else:
            common_options['json'] = self.data
        return common_options

    @property
    def method(self) -> str:
        return self.__method

    @method.setter
    def method(self, value: Literal['GET', 'POST', 'JSON_POST']) -> None:
        if value.upper() not in ['GET', 'POST', 'JSON_POST']:
            raise TypeError("The type of data requested is unknown, Available types:['GET', 'POST', 'JSON_POST']")
        self.__method = value.upper()

    def copy(self) -> 'Request':
        return copy(self)
