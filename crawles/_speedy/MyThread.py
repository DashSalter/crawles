from threading import Thread


class MyThread(Thread):
    def __init__(self, func, *args, **kwargs):
        """
        多线程继承封装
        快速封装功能，增加多线程
        :param func: 函数
        :param args:
        """
        super().__init__()

        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.daemon = True
        # self.setDaemon(True)  # 守护
        self.start()  # 启动线程，调用run

    def run(self):
        self.func(*self.args, **self.kwargs)


def decorator_thread(func):
    """多线程装饰器，用于装饰单个函数"""
    def inner(*args, **kwargs):
        return MyThread(func, *args, **kwargs)

    return inner
