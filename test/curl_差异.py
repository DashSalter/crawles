from crawles import curl_differ

a = '''
curl "https://www.meishij.net/chufang/diy/jiangchangcaipu/" ^
  -H "authority: www.meishij.net" ^
  -H "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7" ^
  -H "accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6" ^
  -H "cache-control: no-cache" ^
  -H "cookie: MSCookieKey=b0fd2a441ac58de8c4cb8b8332ed5ea7.; Hm_lvt_01dd6a7c493607e115255b7e72de5f40=1698914854,1700028804; Hm_lpvt_01dd6a7c493607e115255b7e72de5f40=1700028804" ^
  -H "pragma: no-cache" ^
  -H "sec-ch-ua: ^\^"Microsoft Edge^\^";v=^\^"113^\^", ^\^"Chromium^\^";v=^\^"113^\^", ^\^"Not-A.Brand^\^";v=^\^"24^\^"" ^
  -H "sec-ch-ua-mobile: ?0" ^
  -H "sec-ch-ua-platform: ^\^"Windows^\^"" ^
  -H "sec-fetch-dest: document" ^
  -H "sec-fetch-mode: navigate" ^
  -H "sec-fetch-site: none" ^
  -H "sec-fetch-user: ?1" ^
  -H "upgrade-insecure-requests: 1" ^
  -H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57" ^
  --compressed
'''

b = '''
curl "https://www.meishij.net/chufang/diy/jiangchangcaipu/" ^
  -H "authority: www.meishij.net" ^
  -H "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7" ^
  -H "accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6" ^
  -H "cache-control: no-cache" ^
  -H "cookie: MSCookieKey=b0fd2a441ac58de8c4cb8b8332ed5ea7.; Hm_lvt_01dd6a7c493607e115255b7e72de5f40=1698914854,1700028804; Hm_lpvt_01dd6a7c493607e115255b7e72de5f40=1700028811" ^
  -H "pragma: no-cache" ^
  -H "sec-ch-ua: ^\^"Microsoft Edge^\^";v=^\^"113^\^", ^\^"Chromium^\^";v=^\^"113^\^", ^\^"Not-A.Brand^\^";v=^\^"24^\^"" ^
  -H "sec-ch-ua-mobile: ?0" ^
  -H "sec-ch-ua-platform: ^\^"Windows^\^"" ^
  -H "sec-fetch-dest: document" ^
  -H "sec-fetch-mode: navigate" ^
  -H "sec-fetch-site: none" ^
  -H "sec-fetch-user: ?1" ^
  -H "upgrade-insecure-requests: 1" ^
  -H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57" ^
  --compressed
'''

curl_differ(a, b)


