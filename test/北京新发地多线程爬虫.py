# coding = utf-8
import crawles


class SavePipeline(crawles.Pipeline):  # 数据存储类
    def __init__(self):         # 初始化文件
        self.file = open('test.txt', 'w+', encoding='utf-8')

    def save_data(self, item):  # 数据存储
        self.file.write(str(item) + '\n')

    def close(self):            # 关闭调用
        self.file.close()


class ThreadSpider(crawles.ThreadPool):
    pipeline_class = SavePipeline  # 存储类
    concurrency = 16           # 并发数量
    for_index_range = (1, 100)   # 初始循环区间

    def start_requests(self, request, index):
        request.cookies = { 
        }
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
            'current': index,
            'limit': '',
            'prodCatid': '',
            'prodName': '',
            'prodPcatid': '',
            'pubDateEndTime': '',
            'pubDateStartTime': '',
        }
        request.url = 'http://www.xinfadi.com.cn/getPriceData.html'
        request.method = 'POST'  # GET POST JSON_POST
        request.timeout = 10
        request.retry.retry_request = True
        yield request

    def parse(self, item, request, response):
        # item:存储对象 request:请求对象 response:响应对象
        # print(response.text)

        item['text'] = response.text
        yield item     # 将数据返回到存储类

        # request.url = 'new_url' # 修改请求对象
        # yield request  # 请求对象返回，再次请求


ThreadSpider()
