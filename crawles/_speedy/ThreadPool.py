from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor, \
    wait, ALL_COMPLETED
from copy import copy
from queue import Queue, Empty
from threading import Lock
from time import sleep
from time import time

from requests.exceptions import Timeout
from requests.models import Response

from .._api.api import post, get


def create_bad_response(status=600, text=b'{}'):
    response = Response()
    response.status_code = status  # 状态
    response._content = text  # 空的数据
    return response


class Pipeline(metaclass=ABCMeta):  # 存储管道类
    concurrency = 10  # 并发数量
    __name__ = 'Pipeline'

    @abstractmethod
    def save_data(self, item):
        pass

    @abstractmethod
    def close(self):
        pass


class Item(dict):  # 传输数据对象
    __name__ = 'Item'


class Request:  # 请求对象类
    __name__ = 'Request'

    def __init__(self):
        self.url = None
        self.cookies = {}
        self.headers = {}
        self.callback = None
        self.method = 'GET'
        self.data = {}
        self.index = 0
        self.retry = 0

    def copy(self):
        return copy(self)


class ThreadPool:  # 线程类
    save_class = None  # 爬虫存储类
    concurrency = 16  # 并发数量
    for_index_range = (1, 2)  # 初始循环区间

    random_user_agent = False  # 随机请求头
    timeout = 3  # 等待时间
    request_sleep = 0  # 请求间隔/秒

    retry_request = False  # 请求重试
    retry_interval = 2  # 重试间隔/秒
    retry_time = 3  # 重试次数/次

    def __init__(self):
        self._qsize = 0  # 队列大小
        self.queue_ = Queue(self._qsize)  # 队列
        self.lock = Lock()  # 锁
        self.request_obj = False  # 请求对象 用于判断请求是否已经完成
        self.timeout_ = 0.2  # 超时断开
        self.fail_request = 0  # 失败请求
        self.run()

    def run(self):
        start_time = time()
        # 创建生产者
        producer = Producer(self)
        producer.start_request_(self.start_requests)  # 启动

        # 创建消费者
        consumer = Consumer(self)
        consumer.run()  # 启动

        producer.wait()  # 等待生产者完成

        self.request_obj = True  # 生产者完成，通知消费者停止

        consumer.wait()  # 等待消费者线程完成

        stop_time = time()
        print(f'运行完成 用时:{round(stop_time - start_time, 2)}秒 '
              f'请求次数:{producer.request_index} 失败请求:{self.fail_request}')

    @abstractmethod
    def start_requests(self, request: Request, index: int):
        pass

    @abstractmethod
    def parse(self, item: Item, request_: Request, response):
        pass


class Producer(ThreadPoolExecutor):  # 生产者
    def __init__(self, pipeline: ThreadPool, *args, **kwargs):
        super().__init__(max_workers=pipeline.concurrency, *args, **kwargs)
        self.pipeline = pipeline
        self.request_index = 0  # 请求次数记录
        self.futures = []  # 任务表

    def wait(self):  # 等待请求线程池完成
        while self.futures:
            completed = [future for future in self.futures if future.done()]
            [self.futures.remove(future) for future in completed]

    def pre_request_callback(self, request):
        if not self.pipeline.random_user_agent:
            return  # 是否使用随机请求头
        from random import choice
        from .user_agent import USER_AGENT_LIST
        request.headers['User-Agent'] = choice(USER_AGENT_LIST)

    def callback_(self, request_: Request) -> None:
        request_.method = request_.method.upper()
        self.pre_request_callback(request_)  # 请求之前调用

        try:
            if request_.method == 'POST':
                response = post(request_.url, data=request_.data, timeout=self.pipeline.timeout)
            elif request_.method == 'JSON_POST':
                response = post(request_.url, json=request_.data, timeout=self.pipeline.timeout)
            elif request_.method == 'GET':
                response = get(request_.url, params=request_.data, timeout=self.pipeline.timeout)
            else:
                raise ValueError(f'request_.method:未知的请求类型{request_.method}:POST/JSON_POST/GET')
        except Timeout as e:
            self.print_(create_bad_response(), request_, error=e)
            return
        except Exception as e:
            self.print_(create_bad_response(), request_, error=e)
            return
        self.print_(response, request_, error='')

        # 回调函数/管道数据判断
        for return_ in request_.callback(Item(), request_, response):
            if return_.__name__ == 'Request':
                return_: Request
                with self.pipeline.lock:  # 全局请求次数锁
                    self.request_index += 1
                    request_.index = self.request_index

                self.futures.append(self.submit(self.callback_, request_.copy()))
                sleep(self.pipeline.request_sleep)

            elif return_.__name__ == 'Item' or isinstance(return_, dict):
                return_: Item
                self.pipeline.queue_.put(return_)

    def print_(self, response, request_, error):
        # 爬取信息显示
        with self.pipeline.lock:
            completed = [future if future.done() else None for future in self.futures]
            none_count = max(completed.count(None), 1) - 1

            if response.status_code < 400:
                print(f'status:{response.status_code} '
                      f'index:{str(request_.index).ljust(3, " ")} '
                      f'待完成:{str(none_count).ljust(3, " ")} {error}')
            elif self.pipeline.retry_request and request_.retry < self.pipeline.retry_time:  # 运行重新尝试
                request_.retry += 1  # 是否进行重试
                sleep(self.pipeline.retry_interval)
                print(f'status:\x1b[1;31;3m{response.status_code}\x1b[0m '
                      f'index:{str(request_.index).ljust(3, " ")} '
                      f'待完成:{str(none_count).ljust(3, " ")} 重试次数:{request_.retry}  {error}')
                self.futures.append(self.submit(self.callback_, request_.copy()))
            else:
                self.pipeline.fail_request += 1
                print(f'status:\x1b[1;31;3m{response.status_code}\x1b[0m '
                      f'index:{str(request_.index).ljust(3, " ")} '
                      f'待完成:{str(none_count).ljust(3, " ")}\n    '
                      f'error_url:{request_.url} error_data:{request_.data}\n    '
                      f'error:{error}')

    def start_request_(self, start_requests) -> None:
        # 初始链接请求
        for index in range(*self.pipeline.for_index_range):
            request = Request()
            for request_ in start_requests(request, index):
                with self.pipeline.lock:
                    self.request_index += 1
                    request_.index = self.request_index

                self.futures.append(self.submit(self.callback_, request_))
                sleep(self.pipeline.request_sleep)


class Consumer(ThreadPoolExecutor):  # 消费者
    def __init__(self, pipeline: ThreadPool, *args, **kwargs):
        self.pipeline = pipeline
        self._consume_list = []  # 消费者列表

        save_class_ = pipeline.save_class  # 存储类
        self.save_class_ = save_class_

        if save_class_ is not None:
            self.save_class_ = save_class_()  # 存储类初始化
            super().__init__(max_workers=self.save_class_.concurrency,
                             *args, **kwargs)
        else:
            super().__init__(*args, **kwargs)

    def check_start(func):
        def inner(*args, **kwargs):
            if args[0].save_class_ is None:
                return  # 检查是否存在储数类，如果有就允许任务启动
            result = func(*args, **kwargs)
            return result

        return inner

    @check_start
    def run(self):
        """运行消费者"""
        self._consume_list = [self.submit(self.data_save_)
                              for _ in range(self.save_class_.concurrency)]

    @check_start
    def wait(self):
        """等待线程完成"""
        wait(self._consume_list, return_when=ALL_COMPLETED)
        self.save_class_.close()  # 关闭文件存储

    @check_start
    def data_save_(self) -> None:  # 数据存储
        while True:
            try:
                items = self.pipeline.queue_.get(timeout=self.pipeline.timeout_)
                if self.pipeline.save_class:
                    self.submit(self.save_class_.save_data, items)
                else:
                    break
            except Empty:
                if self.pipeline.request_obj:  # 请求队列完成了，可以结束了
                    break
            except Exception as e:
                print(e)

    check_start = staticmethod(check_start)
