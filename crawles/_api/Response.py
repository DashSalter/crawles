from re import findall

from requests.models import Response

try:
    from lxml import etree
except:
    raise TypeError('lxml 模块异常')


class Response(Response):
    def __init__(self, response):
        self.response = response

    def xpath(self, pattern):
        try:
            html = etree.HTML(self.response.text)
            return html.xpath(pattern)
        except:
            raise TypeError('数据转换异常异常!: etree.HTML(self.response.text)')

    def findall(self, pattern, flags=0):
        if isinstance(flags, str) and str(flags).lower() == 's':
            flags = 16
        return findall(pattern, self.response.text, flags=flags)

    @property
    def json(self):
        try:
            return self.response.json()
        except Exception:
            raise TypeError('该响应体数据不能转换为字典格式！请检查数据格式是否为字典类型')
