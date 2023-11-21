from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor, \
    wait, ALL_COMPLETED
from copy import copy
from queue import Queue, Empty
from threading import Lock
from time import time

from requests.exceptions import Timeout

from .._api.api import post, get


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

    def copy(self):
        return copy(self)


class ThreadPool:  # 线程类
    save_class = None  # 爬虫存储类
    concurrency = 16  # 并发数量
    timeout = 3  # 等待时间
    info_display = True  # 爬取信息显示
    for_index_range = (1, 2)  # 初始循环区间

    def __init__(self):
        self._qsize = 0  # 队列大小
        self.queue_ = Queue(self._qsize)  # 队列
        self.lock = Lock()  # 锁
        self.request_obj = False  # 请求对象 用于判断请求是否已经完成
        self.timeout_ = 0.2  # 超时断开
        self.run()

    def record_run_time(func):
        def inner(*args, **kwargs):
            start_time = time()
            result = func(*args, **kwargs)
            stop_time = time()

            if args[0].info_display:
                print(f'运行用时:{round(stop_time - start_time, 2)}秒 '
                      f'请求次数:{result}')

            return result

        return inner

    @record_run_time
    def run(self):
        # 创建生产者
        producer = Producer(self)
        producer.start_request_(self.start_requests)  # 启动

        # 创建消费者
        consumer = Consumer(self)
        consumer.run()  # 启动

        producer.wait()  # 等待生产者完成

        self.request_obj = True  # 生产者完成，通知消费者停止

        consumer.wait()  # 等待消费者线程完成

        return producer.request_index

    @abstractmethod
    def start_requests(self, request: Request, index: int):
        pass

    @abstractmethod
    def parse(self, item: Item, request_: Request, response):
        pass

    record_run_time = staticmethod(record_run_time)


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

    def callback_(self, request_: Request) -> None:

        request_.method = request_.method.upper()
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
            print(f'RequestTimeout:{e}')
            return
        except Exception as e:
            print(f'RequestError:{e}')
            return

        # 爬取信息显示
        if self.pipeline.info_display:
            with self.pipeline.lock:
                print(f'status:{response} index:{request_.index}')

        # 回调数据获取
        for return_ in request_.callback(Item(), request_, response):
            if return_.__name__ == 'Request':
                return_: Request
                with self.pipeline.lock:  # 全局请求次数锁
                    self.request_index += 1
                    request_.index = self.request_index
                self.futures.append(self.submit(self.callback_, request_.copy()))

            elif return_.__name__ == 'Item' or isinstance(return_, dict):
                return_: Item
                self.pipeline.queue_.put(return_)

    def start_request_(self, start_requests) -> None:
        # 初始链接请求
        for index in range(*self.pipeline.for_index_range):
            request = Request()
            for request_ in start_requests(request, index):
                with self.pipeline.lock:
                    self.request_index += 1
                    request_.index = self.request_index
                self.futures.append(self.submit(self.callback_, request_))


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
