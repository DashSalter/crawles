from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor, \
    wait, ALL_COMPLETED
from copy import copy
from queue import Queue, Empty
from threading import Lock
from time import sleep
from time import time
from types import GeneratorType
from requests.models import Response

from .._api.api import post, get


class BadResponse(Response):
    def __init__(self, status=600, text=b'{}'):
        super().__init__()
        self.status_code = status  # 状态
        self._content = text  # 空的数据


class Pipeline(metaclass=ABCMeta):  # 存储管道类
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
        self.data = {}
        self.callback = None  # 回调函数
        self.method = 'GET'
        self.index = 0  # 绑定索引
        self.retry = 0  # 重试次数
        self.info = ''  # 输出提示信息
        self.proxies = None

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
    retry_interval = 1  # 重试间隔/秒
    retry_time = 3  # 重试次数/次

    print_out = True  # 控制台运行信息
    print_result = True  # 运行结果输出

    def __init__(self):
        self._qsize = 0  # 队列大小
        self.fail_request = 0  # 失败请求数量
        self.queue_ = Queue(self._qsize)  # 队列
        self.lock = Lock()  # 锁
        self.request_obj = False  # 请求对象 用于判断请求是否已经完成
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
        if self.print_result:
            print(f'result:[用时:{round(stop_time - start_time, 2)}秒 '
                  f'请求次数:{producer.request_index} 失败请求:{self.fail_request}]')

    def pre_request_callback(self, request):
        """预请求回调"""
        if not self.random_user_agent:
            return  # 是否使用随机请求头
        from random import choice
        from .user_agent import USER_AGENT_LIST
        request.headers['User-Agent'] = choice(USER_AGENT_LIST)

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
        self.bad_response = BadResponse()

    def wait(self):  # 等待请求线程池完成
        while self.futures:
            completed = [future for future in self.futures if future.done()]
            [self.futures.remove(future) for future in completed]

    def callback_(self, request_: Request) -> None:
        request_.method = request_.method.upper()
        self.pipeline.pre_request_callback(request_)  # 请求之前调用

        start = time()
        try:
            if request_.method == 'POST':
                response = post(request_.url, data=request_.data,
                                proxies=request_.proxies,
                                timeout=self.pipeline.timeout)
            elif request_.method == 'JSON_POST':
                response = post(request_.url, json=request_.data,
                                proxies=request_.proxies,
                                timeout=self.pipeline.timeout)
            elif request_.method == 'GET':
                response = get(request_.url, params=request_.data,
                               proxies=request_.proxies,
                               timeout=self.pipeline.timeout)
            else:
                raise ValueError(f'request_.method:未知的请求类型{request_.method}:POST/JSON_POST/GET')

            self.print_(response, request_, time() - start, error='')
        except Exception as e:
            self.print_(self.bad_response, request_, time() - start, error=e)
            return

        generator = request_.callback(Item(), request_, response)
        if not isinstance(generator,GeneratorType):
            raise TypeError("The returned object is not a generator, use 'yield' as the return keyword")

        # 回调函数/管道数据判断
        for return_ in generator:
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

    def print_(self, response: Response, request_, take_time, error):
        # 爬取信息显示
        with self.pipeline.lock:
            # 获取当前任务数量
            completed = [future if future.done() else None for future in self.futures]
            none_count = max(completed.count(None), 1) - 1

            print_dict = {
                '状态': None,
                '索引': str(request_.index).ljust(3, " "),
                '待完成': str(none_count).ljust(3, " "),
                '用时': f'{take_time:.2f}',
                'error': error, 'info': request_.info
            }

            if response.status_code < 400:
                print_dict['状态'] = response.status_code

            elif self.pipeline.retry_request and request_.retry <= self.pipeline.retry_time:  # 运行重新尝试
                request_.retry += 1  # 是否进行重试
                sleep(self.pipeline.retry_interval)  # 重试请求间隔
                print_dict['状态'] = f'\x1b[1;31;3m{response.status_code}\x1b[0m'
                print_dict['重试'] = request_.retry

                self.futures.append(self.submit(self.callback_, request_.copy()))
            else:
                self.pipeline.fail_request += 1  # 请求失败纪录
                print_dict['状态'] = f'\x1b[1;31;3m{response.status_code}\x1b[0m'
                print_dict['error_data'] = request_.data
                print_dict['error_url'] = request_.url

            if self.pipeline.print_out:
                print(''.join([f'{k}:{v}\t' for k, v in print_dict.items() if v]))

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
        self.timeout_ = 0.2  # 消费者超时断开
        save_class_ = pipeline.save_class  # 存储类
        self.save_class_ = save_class_
        self.concurrency = 10
        if save_class_ is not None:
            self.save_class_ = save_class_()  # 存储类初始化
        super().__init__(max_workers=self.concurrency, *args, **kwargs)

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
                              for _ in range(self.concurrency)]

    @check_start
    def wait(self):
        """等待线程完成"""
        wait(self._consume_list, return_when=ALL_COMPLETED)
        self.save_class_.close()  # 关闭文件存储

    @check_start
    def data_save_(self) -> None:  # 数据存储
        while True:
            try:
                items = self.pipeline.queue_.get(timeout=self.timeout_)
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
