

from crawles import curl_differ

a = '''
curl "http://www.xinfadi.com.cn/getPriceData.html" ^
  -H "Accept: */*" ^
  -H "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6" ^
  -H "Cache-Control: no-cache" ^
  -H "Connection: keep-alive" ^
  -H "Content-Type: application/x-www-form-urlencoded; charset=UTF-8" ^
  -H "Origin: http://www.xinfadi.com.cn" ^
  -H "Pragma: no-cache" ^
  -H "Referer: http://www.xinfadi.com.cn/priceDetail.html" ^
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57" ^
  -H "X-Requested-With: XMLHttpRequest" ^
  --data-raw "limit=20&current=2&pubDateStartTime=&pubDateEndTime=&prodPcatid=&prodCatid=&prodName=" ^
  --compressed ^
  --insecure
'''

b = '''
curl 'http://www.xinfadi.com.cn/getPriceData.html' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.7' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'Origin: http://www.xinfadi.com.cn' \
  -H 'Pragma: no-cache' \
  -H 'Referer: http://www.xinfadi.com.cn/priceDetail.html' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57' \
  -H 'X-Requested-With: XMLHttpRequest' \
  --data-raw 'limit=20&current=3&pubDateStartTime=&pubDateEndTime=&prodPcatid=&prodCatid=&prodName=' \
  --compressed \
  --insecure
'''

curl_differ(a, b)


