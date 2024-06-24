from re import findall, search, I
from lxml import etree
from typing import Literal
import sre_compile
from curl_cffi.requests import models


def error_print(error):  # 异常输出
    print(f"\033[91m{error}\033[0m")


class Response(models.Response):
    def __init__(self, response):
        self.response = response
        self.elapsed = 0.0
        self.flags_dict = {
            'A': sre_compile.SRE_FLAG_ASCII,
            'I': sre_compile.SRE_FLAG_IGNORECASE,
            'L': sre_compile.SRE_FLAG_LOCALE,
            'U': sre_compile.SRE_FLAG_UNICODE,
            'M': sre_compile.SRE_FLAG_MULTILINE,
            'S': sre_compile.SRE_FLAG_DOTALL,
            'X': sre_compile.SRE_FLAG_VERBOSE,
            'T': sre_compile.SRE_FLAG_TEMPLATE,
            'DEBUG': sre_compile.SRE_FLAG_DEBUG,
        }
        tips_data = search(r'<title>Just a moment\.\.\.</title>', self.response.text, I)
        # TLS 指纹拦截提示

        if tips_data and self.response.status_code == 403:
            error_print("The request failed, "
                        "The website intercepts the request using TLS fingerprinting!")
            error_print("You can try it: response = crawles.get(url, impersonate='chrome110')")

    def xpath(self, pattern):
        if pattern:
            html = etree.HTML(self.response.text)
            return html.xpath(pattern)

    def findall(self, pattern, flags: Literal['A', 'I', 'L', 'U', 'M', 'S', 'X', 'T', 'DEBUG'] = 0):
        if flags != 0:
            if not self.flags_dict.get(str(flags).upper()):
                raise ValueError('There is no such matching method in flags')
            else:
                flags = self.flags_dict[str(flags).upper()]
        return findall(pattern, self.response.text, flags=flags)

    def save(self, file_name, encoding='utf-8'):
        with open(file_name, 'w+', encoding=encoding) as file:
            file.write(self.response.text)

    def __str__(self):
        return f'<Response status_code:{self.response.status_code}>'


class BadResponse(models.Response):  # 请求错误返回响应体
    def __init__(self, status=600, text=b'{}'):
        super().__init__()
        self.elapsed = 0.0
        self.status_code = status  # 状态
        self._content = text  # 空的数据
