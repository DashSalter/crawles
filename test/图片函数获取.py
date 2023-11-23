# coding = utf-8
import crawles

url = 'https://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi'

cookies = {
    'RK': 'YmdZHPHIR7',
    'ptcz': '31de8e05cbbaf25ae452675851770c8a1c297f011b97efc2ae7b35cf65a7de98',
    'pac_uid': '0_7f8048ef3ca3f',
    'iip': '0',
    'eas_sid': '11p6C9c7Z297x2N8s0d5X9J2a3',
    'LW_uid': 'a1z6c9I7t257Z2F8q066d2K3Y0',
    'pgv_pvid': '7146443171',
    'luin': 'o1431705288',
    'lskey': '00010000067a69cf8268f83cac081eddff25d1dde1317cb9b4f68616cc5eda6407af2d1eddee3299ad9ee322',
    'LW_sid': 'D1P6M9T8N733i5S7A9d0D1z4b3',
    'pgv_info': 'ssid=s3625732087',
    'pvpqqcomrouteLine': 'index_wallpaper',
}

headers = {
    'authority': 'apps.game.qq.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://pvp.qq.com/',
    'sec-ch-ua': '\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\"Windows\"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',
}
from time import time

a = time()
for page in range(1, 2):
    params = {
        'activityId': '2735',
        'sVerifyCode': 'ABCD',
        'sDataType': 'JSON',
        'iListNum': '20',
        'totalpage': '0',
        'page': page,
        'iOrder': '0',
        'iSortNumClose': '1',
        'iAMSActivityId': '51991',
        '_everyRead': 'true',
        'iTypeId': '2',
        'iFlowId': '267733',
        'iActId': '2735',
        'iModuleId': '2735',
        '_': '1698735793566',
    }

    # 当前时间戳: 1698735867.234549
    response = crawles.get(url, headers=headers, params=params, cookies=cookies)
    from urllib import parse, request
    d = {}
    for i in response.json['List']:
        image_name = i['sProdName']  # 获取名字
        image_name = parse.unquote(image_name)  # 解析名称
        for j in range(2, 9):  # 获取2-8的图片链接
            url_data = parse.unquote(i[f'sProdImgNo_{j}']).replace('jpg/200', 'jpg/0')  # 解析网址
            d[url_data] = 'image/' + image_name + f'_{j}.png'
            # request.urlretrieve(url_data, 'image/' + image_name + '.png')
            # print(url_data)
    crawles.image_save(d)
b = time()
print(b - a)

# 81.75303649902344
# 8
