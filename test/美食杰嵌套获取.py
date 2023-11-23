# coding = utf-8
import crawles


class SavePipeline(crawles.Pipeline):  # 数据存储类
    def __init__(self):  # 初始化文件
        self.file = open('test.txt', 'w+', encoding='utf-8')

    def save_data(self, item):  # 数据存储
        self.file.write(str(item) + '\n')

    def close(self):  # 关闭调用
        self.file.close()


class ThreadSpider(crawles.ThreadPool):
    save_class = SavePipeline  # 存储类
    concurrency = 16  # 并发数量
    for_index_range = (1, 3)  # 初始循环区间
    timeout = 20  # 等待时间
    retry_request = True  # 爬取重试

    def start_requests(self, request, index):
        request.cookies = {
            'Hm_lpvt_f4fa5d56f272ae0a0777feec2184a97f': '1700029239',
            'Hm_lvt_f4fa5d56f272ae0a0777feec2184a97f': '1700029239',
            'XSRF-TOKEN': 'eyJpdiI6IlVZV1I3U05wdEUranZ2cWc0bkFqZXc9PSIsInZhbHVlIjoiVVRLa1wvRHd4MklIYmp5TmpiUUM0aFdUZ21QVURvWUVwaFFmNkFwQVN2TmZ2dVlTTWYyb2JoYXY1QmZSQXlZVXgiLCJtYWMiOiI2YjllZmFmMDliYzBkZjlmMzJmNjA5MmU1YWQzNzg2MmFjNmI4NDQzZjM0MjNmMmM0NDJiOTFkZDllYjlhODUwIn0%3D',
            'https_waf_cookie': 'f836e8ae-f402-4bea225cbdd23e3cc44e13aded2614393ffb',
            'laravel_session': '6yqgGDlc8q6qqJT4unwEc5evx1JU5Hgu1TImtxHo',
        }
        request.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',
            'sec-ch-ua': '\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '\"Windows\"',
        }
        request.data = {
        }
        request.url = f'https://www.douguo.com/jingxuan/{index}'
        request.method = 'GET'  # GET POST JSON_POST
        request.callback = self.parse
        yield request

    def parse(self, item, request, response):
        # item:存储对象 request:请求对象 response:响应对象
        # print(response.text)

        data = response.findall('<a class="cover" href="(.*?)" target="_blank" style="position: relative">')
        for i in data:
            request.url = f'https://www.douguo.com{i}'
            request.callback = self.ap
            yield request

    def ap(self, item, request, response):
        data = (response.findall('<h2 class="mini-title">(.*?)</h2>'))
        item['data'] = data
        yield item


ThreadSpider()
