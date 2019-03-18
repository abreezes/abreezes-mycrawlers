import demjson
import gevent
import requests
import cookiesopertion
from fake_useragent import UserAgent
from gevent import monkey
import pymysql
from gevent import queue
monkey.patch_all()


class CrawlComId:
    def __init__(self):
        self.con=pymysql.Connect(host='127.0.0.1',user='root',password='root',port=3306,database='jobble')
        self.cursor = self.con.cursor()

        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'http://radar.itjuzi.com/company',
            'X-Requested-With': 'XMLHttpRequest',
            'Proxy-Connection': 'keep-alive',
        }
        self.base_url = 'http://radar.itjuzi.com/company/infonew?page={}'
        self.random_cookie=cookiesopertion.LoginGetCookies()
        self.ua=UserAgent()
        self.xclist = [[],[],[],[],[],[],[],[],[],[]]


    @property
    def get_page_count(self,page=1):
        """获取总页数"""
        res=self.download(self.base_url.format(page))
        page=res['data']['page_total']
        return page

    @property
    def gen_page_url(self):
        """生成page url列表"""
        return [self.base_url.format(page) for page in range(1,self.get_page_count+1)]

    def download(self,url):
        """下载器"""
        proxies = {
            "http": "http://H42042607409G18D:892940E3D729B818@http-dyn.abuyun.com:9020/",
        }
        cookies = self.random_cookie.random_file
        self.headers['User-Agent'] = self.ua.random
        gevent.sleep(1.5)
        try:
            res = requests.get(url=url, headers=self.headers, cookies=cookies,proxies=proxies).json()
            if res:
                return res
        except Exception as e:
            with open('urlerr.txt','a+') as f:
                f.write(url)
                f.write('\n')
            with open('urlexp.txt', 'a+') as f:
                f.write(str(e))
                f.write('\n')
                pass


    def parse(self,url_list):
        """解析器"""
        for url in url_list:
            res=self.download(url)
            try:
                infos=res['data']['rows']
                if infos:
                    for row in infos:
                        #self.task.put(row['com_id'])
                        self.insert_mysql(row['com_id'])
                else:
                    with open('parseerr.txt', 'a+') as f:
                        f.write(str(url))
                        f.write('\n')
                    continue

            except Exception as e:
                with open('parseexp.txt', 'a+') as f:
                    f.write(str(e))
                    f.write('\n')
                pass

    def insert_mysql(self,id):
            sql = 'INSERT INTO juzi (com_id) VALUES ({});'.format(id)
            try:
                if self.cursor.execute(sql):
                    self.con.commit()
                    print('Successful')
            except Exception as e:
                print(e)
                print('Failed')

    def fenge_task(self):
        # 协程任务切割
        print(len(self.gen_page_url))
        url_list = self.gen_page_url
        n = len(self.xclist)
        for i in range(len(url_list)):
            self.xclist[i % n].append(url_list[i])

    def engine(self):
        """开启协程"""
        self.fenge_task()
        n = len(self.xclist)
        task_list = []
        for i in range(n):
            task_list.append(gevent.spawn(self.parse, self.xclist[i]))
        # 等待
        gevent.joinall(task_list)
        self.con.close()


    #
    # res=requests.get('https://www.itjuzi.com/company/33428566',headers=headers).text
    # print(res)1



if __name__ == '__main__':
    CrawlComId().engine()


