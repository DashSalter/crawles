# coding = utf-8
import crawles


class SavePipeline(crawles.Pipeline):  # 数据存储类
    def __init__(self):  # 初始化文件
        self.file = open('test.txt', 'w+', encoding='utf-8')

    def save_data(self, item):  # 数据存储
        self.file.write(str(item) + '\n')

    def close(self):  # 关闭调用
        self.file.close()


class ThreadSpier(crawles.ThreadPool):
    pipeline_class = None  # 存储类
    concurrency = 16  # 并发数量

    def start_requests(self, request, index):
        request.headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://www.xinfadi.com.cn',
            'Pragma': 'no-cache',
            'Referer': 'http://www.xinfadi.com.cn/priceDetail.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',
            'X-Requested-With': 'XMLHttpRequest',
        }

        request.data = {
            'limit': '20',
            'current': 1,
            'pubDateStartTime': '',
            'pubDateEndTime': '',
            'prodPcatid': '',
            'prodCatid': '',
            'prodName': '',
        }
        request.url = 'http://www.xinfadi.com.cn/getPriceData.html'
        request.method = 'POST'
        yield request

    def parse(self, item, request, response):
        # item:存储对象 request:请求对象 response:响应对象
        # print(response.text)

        item['json'] = response.json()
        yield item  # 将数据返回到存储类

        request.data['current'] += 1
        if request.data['current'] <= 20:
            yield request  # 请求对象返回


ThreadSpier()
