from typing import Text


class ExecJs:
    def __init__(self, filename):
        self.__js_compile = None

    def call(self, func, *args, **kwargs): pass


def execjs(filename: Text) -> ExecJs: pass
