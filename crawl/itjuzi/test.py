import requests
import cookiesopertion
import demjson
from gevent import monkey
monkey.patch_all()
import gevent
from gevent import queue


proxies = {
    "http": "http://H42042607409G18D:892940E3D729B818@http-dyn.abuyun.com:9020/",
}

headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'http://radar.itjuzi.com//company',
    'X-Requested-With': 'XMLHttpRequest',
    'Proxy-Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

filecookies=cookiesopertion.LoginGetCookies()
cookies=filecookies.random_file
print(cookies)
print(type(cookies))

res = requests.get('http://radar.itjuzi.com/company/infonew?page=1077', headers=headers,cookies=cookies).text
res=demjson.decode(res)

print(res['data']['page_total'])




