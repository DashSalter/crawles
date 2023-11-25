# coding = utf-8
import requests

from crawles import CsvOpen

with CsvOpen('北京新发地.csv', 'w+') as f:
    for page in range(1, 11):
        url = 'http://www.xinfadi.com.cn/getPriceData.html'

        cookies = {
        }

        headers = {
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

        data = {
            'current': page,
            'limit': '20',
            'prodCatid': '',
            'prodName': '',
            'prodPcatid': '',
            'pubDateEndTime': '',
            'pubDateStartTime': '',
        }

        # 当前时间戳: 1700897148.143121
        response = requests.post(url, headers=headers, data=data, cookies=cookies)
        print(response.text)

        f.writerows(response.json()['list'])
