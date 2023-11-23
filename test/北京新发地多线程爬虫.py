# coding = utf-8
import crawles


class SavePipeline(crawles.Pipeline):  # 数据存储类
    def __init__(self):         # 初始化文件
        pass  # self.file = open('test.txt', 'w+', encoding='utf-8')

    def save_data(self, item):  # 数据存储
        pass  # self.file.write(str(item) + '\n')

    def close(self):            # 关闭调用
        pass  # self.file.close()


class ThreadSpider(crawles.ThreadPool):
    save_class = SavePipeline  # 存储类
    concurrency = 16           # 并发数量
    info_display = True        # 爬取信息显示
    for_index_range = (1, 10)         # 初始循环区间

    def start_requests(self, request, index):
        request.cookies = { 
            'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1700556079',
            'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1700485319,1700556079',
            '_ga': 'GA1.2.1193088964.1700556082',
            '_ga_4JBJY7Y7MX': 'GS1.2.1700556082.1.0.1700556082.0.0.0',
            '_gat': '1',
            '_gat_dianpu_agent': '1',
            '_gat_global': '1',
            '_gat_new_global': '1',
            '_gid': 'GA1.2.769867899.1700556082',
            '_jzqa': '1.3366939842336027600.1700556080.1700556080.1700556080.1',
            '_jzqb': '1.1.10.1700556080.1',
            '_jzqc': '1',
            '_jzqckmp': '1',
            '_qzja': '1.1200595011.1700485320657.1700485320658.1700556080885.1700486097372.1700556080885.0.0.0.9.2',
            '_qzjb': '1.1700556080885.1.0.0.0',
            '_qzjc': '1',
            '_qzjto': '1.1.0',
            '_smt_uid': '655c6d2f.2bf9f973',
            'lianjia_ssid': '8775b4ee-84be-4009-b6e0-6270fae23568',
            'lianjia_uuid': 'b5bb5fe9-3bde-4d27-b458-5e8ba4c2bdcb',
            'sajssdk_2015_cross_new_user': '1',
            'select_city': '430100',
            'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2218bf10a80fe117-05fdca5e1f9d29-7b515473-1327104-18bf10a80ff987%22%2C%22%24device_id%22%3A%2218bf10a80fe117-05fdca5e1f9d29-7b515473-1327104-18bf10a80ff987%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D',
            'srcid': 'eyJ0Ijoie1wiZGF0YVwiOlwiNmFiMjJmZmNmOTFiZWFkMGJiMTk5YjhiZDQ3MTAzNWY5NmY1MjRjNDllMTY5MmUyYzQ0Nzk2YTIxZDg3OTI1OTA2NzBhODUwZThmZWJmMzllMDhmNTRkOThhYzcxMmRmZDAwODhjNmI1ZGM5NTA4MTk4MTY5ZGNhMTFmZGUyNDc4MWQ5M2ZhMDg2YjE4MmVmODFmODIwZGNhNmY2NjBlZGI0Nzc1MDA2MzhiZmVkMzY0MmFlMzRhYzk5OTAyN2NiYmQ3ZTBkNjA2YzIxNTBlN2QzYTdjMjdlOGU5YmFjOGZjNGM2YWMwZjljNWYwYjM1ODc1Yjk5OGQwYzc5MGIwOFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI4NmUxMWFkOVwifSIsInIiOiJodHRwczovL2NzLmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvcGcxLyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9',
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
        request.url = f'https://cs.lianjia.com/ershoufang/pg{index}/'
        request.method = 'GET'  # GET POST JSON_POST
        request.callback = self.parse
        yield request

    def parse(self, item, request, response):
        # item:存储对象 request:请求对象 response:响应对象
        # print(response.text)
        pass
        # item['text'] = response.text
        # yield item     # 将数据返回到存储类

        # request.url = 'new_url' # 修改请求对象
        # yield request  # 请求对象返回，再次请求


ThreadSpider()
