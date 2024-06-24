**当前方法以及功能** 

header_format:
- 将字符串格式的请求头数据转换为字典

```python
    data1 = '''
    :Accept: */*
    Accept-Encoding:zh-CN,zh;q=0.9
    X-Requested-With      :   XMLHttpRequest
    sec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "Windows"
    '''
    import crawles
    crawles.op(crawles.header_format(data1))
```
```
{
  'Accept': '*/*',
  'Accept-Encoding': 'zh-CN,zh;q=0.9',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}
```