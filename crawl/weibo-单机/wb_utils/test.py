import time

import random

def generade_id():
    for id in range(2, 36):
        # yield from gen_ch(id)
        yield id



# def gen_ch(id):
#     li=[1,5,1,9,10,8,9,4,55]
#
#     yield random.choice(li)+id
g=generade_id()

def s():
    import requests

    cookies = {
        'SINAGLOBAL': '9910109870667.902.1544253208794',
        '_ga': 'GA1.2.1198700794.1544258648',
        'UOR': ',,login.sina.com.cn',
        'SCF': 'Alwg39kt1vdIAaxmAcAhzaIv3sj928wGq198xPR1BYTxeRPRz6prW6z3yeFDy7wNlFe8iR43gWXNskrIjIQLOrI.',
        'SUHB': '0z1Qm2PIjMA3mq',
        'login_sid_t': '1055bc83883685400ca32f5ea156a79a',
        'cross_origin_proto': 'SSL',
        'Ugrow-G0': '9642b0b34b4c0d569ed7a372f8823a8e',
        'YF-V5-G0': 'b59b0905807453afddda0b34765f9151',
        '_s_tentry': '-',
        'Apache': '8240258368460.971.1544329972571',
        'ULV': '1544329973265:3:3:1:8240258368460.971.1544329972571:1544258653051',
        'SUB': '_2AkMrUH1idcPxrAVXkPsXxGziZIlH-jyYhRSUAn7uJhMyOhh77kguqSVutBF-XDv0TcmjyjWh7nGtbmz7gMxSLEy1',
        'SUBP': '0033WrSXqPxfM72wWs9jqgMF55529P9D9W5CYW3czC4CkFzyqmyKuKxR5JpVsNiE9svQdoM0SozE1-WrqgfLTrULIgiaTJSadBtt',
        'WBStorage': 'bfb29263adc46711|undefined',
        'wb_view_log': '1366*7681',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=https%3A%2F%2Fweibo.com%2F&domain=.weibo.com&ua=php-sso_sdk_client-0.6.28&_rand=1544352340.1551',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'If-Modified-Since': 'Sun, 09 Dec 2018 10:45:41 GMT',
    }
    proxies = {
        "http": "http://114.238.135.120:59412",
        "https": "http://114.238.135.120:59412",
    }

    response = requests.get('https://weibo.com/', headers=headers,proxies=proxies)
    print(response.text)
    print(response.status_code)
    if response.status_code == 200:
        print(proxies)


def t():
    import requests
    flag=True
    while flag:
        # res=requests.get('http://api.ip.data5u.com/dynamic/get.html?order=9b82eeeb939413e3b287a1f2d5c508e1&json=1&sep=3').json()
        # print(res)
        # print(res['data'][0]['ip'])
        # time.sleep(4)
        res=requests.get('http://api.ip.data5u.com/dynamic/get.html?order=9b82eeeb939413e3b287a1f2d5c508e1&random=true&sep=3')
        print(res.text)
        time.sleep(5)

if __name__ == '__main__':
    s()



