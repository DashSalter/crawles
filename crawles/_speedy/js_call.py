from typing import Union

import execjs as j


class ExecJs:
    def __init__(self, filename: Union[str, bytes]):
        self.filename = filename
        f = open(self.filename, 'r', encoding='utf-8')
        self.js_data = f.read()
        f.close()

        self.__js_compile = j.compile(self.js_data)

    def call(self, func, *args, **kwargs):
        return self.__js_compile.call(func, *args, **kwargs)


execjs = ExecJs

if __name__ == '__main__':
    js = execjs('1')
    # 使用js函数
    result = js.call('func/函数名', '参数1', '参数2', '参数......')
