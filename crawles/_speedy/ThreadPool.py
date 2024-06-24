from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from os import kill, getpid
from queue import Queue, Empty
from threading import Lock
from time import sleep, time
from types import GeneratorType
from typing import Union
from traceback import format_exc
from .Response import Response,BadResponse
from .RFPDupeFilter import RFPDupeFilter  # 过滤器
from .Request import Request


def error_print(error):  # 异常输出
    print(f"\033[91m{error}\033[0m")


# 传输数据Item对象
Item = type('Item', (dict,), {})


class Pipeline(metaclass=ABCMeta):
    # 存储管道抽象类
    @abstractmethod
    def save_data(self, item: dict): pass

    @abstractmethod
    def close(self): pass


class ThreadPool:  # 线程类
    pipeline_class = None  # 爬虫存储类
    concurrency = 16  # 并发数量
    for_index_range = (1, 2)  # 初始循环区间

    print_out = True  # 控制台运行信息
    print_result = True  # 运行结果输出
    fail_request_log = False  # 失败请求记录日志

    DupeFilter = RFPDupeFilter(file_path=None)  # 重复过滤器 存储运行内存
    '''
    from crawles import RFPDupeFilter  # 断点续爬
    DupeFilter = RFPDupeFilter(file_path='requests.seen')  # 本地存储路径
    '''

    def __init__(self):
        self.producer = Producer(self)  # 创建生产者
        self.consumer = Consumer(self)  # 创建消费者
        self.fail_request_set = set()  # 请求失败对象集合
        self.request_obj = False  # 请求对象 用于判断请求是否已经完成
        self.fail_request = 0  # 失败请求数量
        self.queue_ = Queue()  # 队列
        self.lock = Lock()  # 锁
        self._start()

    def _run(self) -> None:
        self.producer.run()  # 生产者启动
        self.consumer.run()  # 消费者启动
        self.producer.wait()  # 等待生产者完成
        self.request_obj = True  # 生产者完成，通知消费者可以停止
        self.consumer.wait()  # 等待消费者线程完成

        self.DupeFilter.close()  # 关闭过滤器

    def _start(self) -> None:
        """运行线程池和最终结果总结"""
        start_time, run, end_time = time(), self._run(), time()
        if self.print_result:  # 结果输出
            print(f'result:[总用时:{round(end_time - start_time, 2)}秒 '
                  f'请求次数:{self.producer.request_index} 失败请求:{self.fail_request}]')

        if self.fail_request_log:  # 失败请求存储
            from re import sub
            with open('fail_request_log.txt', 'w+', encoding='utf-8') as file:
                for fail_request in self.fail_request_set:
                    fail_request_str = sub('\x1b\[\d+m', "", str(fail_request))
                    file.write(f'{fail_request_str}\n')

    @abstractmethod
    def start_requests(self, request: Request, index: int):
        pass  # 初始化请求参数

    @abstractmethod
    def parse(self, item: Item, request: Request, response: Response):
        pass  # 数据解析

    def error_request(self, request: Request):
        pass  # 失败请求对象


class Producer(ThreadPoolExecutor):  # 生产者
    def __init__(self, pipeline: ThreadPool, *args, **kwargs):
        super().__init__(max_workers=pipeline.concurrency, *args, **kwargs)
        self.pipeline = pipeline
        self.request_index = 0  # 请求次数记录
        self.futures = []  # 任务表
        self.bad_response = BadResponse()

    def wait(self):  # 等待请求线程池完成
        try:
            while self.futures:
                completed = [future for future in self.futures if future.done()]
                [self.futures.remove(future) for future in completed]
                # done(): Return True if the call was successfully cancelled or finished running
        except KeyboardInterrupt:
            error_print('KeyboardInterrupt: The thread pool program was forcibly terminated!')
            kill(getpid(), 0)  # 结束当前进程
        finally:
            self.shutdown()

    @staticmethod
    def error_message(_):  # 获取报错信息
        return error_print(format_exc())

    def callback_(self, request_: Request) -> None:
        request_.pre_request_callback(request_)  # 请求之前调用
        try:  # 请求
            response = request_.make_request()
            self.print_(response, request_, error='')
        except Exception as e:
            self.print_(self.bad_response, request_, error=e)
            return

        try:  # 回调函数调用
            generator: GeneratorType = request_.callback(Item(), request_, response)
        except Exception as e:
            return self.error_message(e)

        if generator is None:
            return  # 是否是生成器已经可用
        elif not isinstance(generator, GeneratorType):
            return error_print("TypeError: The returned object is not a generator, "
                               "use 'yield' as the return keyword")

        try:  # 回调生成器处理
            # 回调返回的生成器数据处理
            self.callback_generator_processing(generator, request_)
        except Exception as e:
            return self.error_message(e)

    def callback_generator_processing(self, generator: GeneratorType, request_: Request):
        for return_ in generator:
            if isinstance(return_, Request):  # 回调函数/管道数据判断
                if self.pipeline.DupeFilter and self.pipeline.DupeFilter.request_seen(request_):
                    continue  # 过滤器 存在则返回True

                # 如果链接未存在
                with self.pipeline.lock:  # 全局请求次数锁
                    self.request_index += 1
                    request_.index = self.request_index

                self.futures.append(self.submit(self.callback_, request_.copy()))
                sleep(request_.request_sleep)

            elif isinstance(return_, (Item, dict)):
                self.pipeline.queue_.put(return_)
            else:
                raise TypeError('The returned object is not a usable object')

    def print_(self, response: Union[Response, BadResponse], request_: Request, error) -> None:
        # 爬取信息显示
        with self.pipeline.lock:
            # 获取当前任务数量
            completed = [future if future.done() else None for future in self.futures]
            none_count = max(completed.count(None), 1) - 1
            print_dict = {
                'ID': str(request_.index),
                '状态': str(response.status_code),
                '待完成': str(none_count),
                '用时': f'{response.elapsed.total_seconds():.2f}', '重试': None,
                'info': request_.info, 'error': error,
            }

            if response.status_code < 400:
                pass
            elif request_.retry.retry_request and request_.current_retry < request_.retry.retry_total:  # 运行重新尝试
                request_.current_retry += 1  # 是否进行重试
                sleep(request_.retry.retry_interval)  # 重试请求间隔
                print_dict['状态'] = f'\x1b[1;31;3m{response.status_code}\x1b[0m'
                print_dict['重试'] = request_.current_retry
                self.futures.append(self.submit(self.callback_, request_.copy()))
            else:
                self.pipeline.fail_request_set.add(request_.copy())
                self.pipeline.fail_request += 1  # 请求失败纪录
                print_dict['状态'] = f'\x1b[1;31;3m{response.status_code}\x1b[0m'
                print_dict['error_data'] = request_.data
                print_dict['error_url'] = request_.url

                self.pipeline.error_request(request_)

            if self.pipeline.print_out:
                print('<' + '  '.join([f'{k}:{v}' for k, v in print_dict.items() if v]) + '>')

    def run(self) -> None:
        # 初始链接请求
        for index in range(*self.pipeline.for_index_range):
            request = Request()
            request.callback = self.pipeline.parse  # 设置默认回调函数
            for request_ in self.pipeline.start_requests(request, index):
                if self.pipeline.DupeFilter and self.pipeline.DupeFilter.request_seen(request_):
                    continue  # 过滤器 存在则返回True

                with self.pipeline.lock:
                    self.request_index += 1
                    request_.index = self.request_index

                self.futures.append(self.submit(self.callback_, request_))
                sleep(request_.request_sleep)


class Consumer(ThreadPoolExecutor):  # 消费者
    def __init__(self, pipeline: ThreadPool, *args, **kwargs):
        self.pipeline = pipeline
        self._consume_list = []  # 消费者列表
        self.timeout_ = 0.2  # 消费者超时断开
        self.save_class = pipeline.pipeline_class  # 存储类
        self.concurrency = 5  # 消费者并发数量
        super().__init__(max_workers=self.concurrency, *args, **kwargs)

        if self.save_class is not None:
            self.save_class = self.save_class()  # 存储类初始化

    def run(self) -> None:
        """运行消费者"""
        self._consume_list = [self.submit(self.data_save_) for _ in range(self.concurrency)]

    def wait(self) -> None:
        """等待线程完成"""
        wait(self._consume_list, return_when=ALL_COMPLETED)
        if self.save_class:  # 关闭存储类
            self.save_class.close()
        self.shutdown()

    def data_save_(self) -> None:  # 数据存储
        while True:
            try:
                items = self.pipeline.queue_.get(timeout=self.timeout_)
                if self.save_class:
                    self.submit(self.save_class.save_data, items)
                else:
                    break
            except Empty:
                if self.pipeline.request_obj:  # 请求队列完成了，可以结束了
                    break
            except Exception as e:
                print(e)
