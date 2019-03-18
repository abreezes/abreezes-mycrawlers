import requests
from fake_useragent import UserAgent
import random
import json
import time



class LoginGetCookies:
    cookies_all = {}

    def __init__(self):
        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'http://radar.itjuzi.com/company',
            'X-Requested-With': 'XMLHttpRequest',
            'Proxy-Connection': 'keep-alive',
        }
        self.session=requests.Session()
        self.acc=open('accounts','r')

        self.ua=UserAgent()
        self.cookies_file=open('cookie.json','a')

    def engine(self):
        """控制所有帐号登录"""
        for acc in self.acc.readlines():
            self.login(acc)

        self.acc.close()
        obj = json.dumps(self.cookies_all, ensure_ascii=False)
        self.cookies_file.write(obj)
        self.cookies_file.close()

    def login(self,acc):
        """登录操作"""
        url = 'https://www.itjuzi.com/user/login?redirect=&flag=&radar_coupon='
        data = {"identity": acc.strip(),
                "password": "abcd123"}
        self.headers['User-Agent']=self.ua.random
        self.session.post(url=url, data=data, headers=self.headers, verify=False)
        if self.check_login(acc):
            print('Success--->%s'%acc)
            self.session.cookies.clear_session_cookies()


    def check_login(self,acc):
        """判断是否登录成功"""
        time.sleep(2)
        res = self.session.get('http://radar.itjuzi.com/company/infonew?page=1', headers=self.headers).json()
        return self.is_login(acc,res)

    def is_login(self,acc,res):
        """判断是否登录"""
        if res['status'] == 1:
            cookie = {}
            cookielist = self.session.cookies.items()
            for i in cookielist:
                cookie[i[0].strip()] = i[1]
            self.cookies_all[acc.strip()]=cookie
            return True

    def check_cookies(self):
        """检查cookies有效性"""
        with open('cookie.json', 'r') as fr:
            obj = json.loads(fr.read())
        for acc,cookies in obj.items():
            self.headers['User-Agent'] =self.ua.random
            res = requests.get('http://radar.itjuzi.com/company/infonew?page=2', headers=self.headers, cookies=cookies).json()
            if not self.is_login(acc,res):
                self.login(acc)

    @classmethod
    def random_cookies(cls):
        """随机返回一个cookie"""
        return cls.cookies_all.get(random.choice(list(cls.cookies_all)))
        #cls.r=dict(cls.cookies_all.get(random.choice(list(cls.cookies_all))))

    @property
    def random_file(self):
        """读取json文件随机返回一个cookie"""
        with open('cookie.json','r') as fr:
            obj = json.loads(fr.read())
            return obj.get(random.choice(list(obj)))


class Register:
    def __init__(self):

        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'http://radar.itjuzi.com/company',
            'X-Requested-With': 'XMLHttpRequest',
            'Proxy-Connection': 'keep-alive',
        }
        self.acc = open('accounts', 'r')


    def register(self):
        for acc in self.acc.readlines():
            data = {'email': acc.strip(),
                    'password': 'abcd123'}
            requests.post('https://www.itjuzi.com/user/register_email?redirect=&flag=', headers=self.headers, data=data,
                               verify=False)




if __name__ == '__main__':

    l=LoginGetCookies()
    # l.engine()
    l.check_cookies()
    for i in range(1,100):
        print(l.random_file)






