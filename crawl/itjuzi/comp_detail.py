import multiprocessing
import threading
import time
import gevent
import pymysql
import requests
from lxml import etree
from gevent import monkey
import itjuzi_helper

monkey.patch_all()




class CrawlCompDetail:

    def __init__(self):
        self.headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://radar.itjuzi.com//company',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'If-Modified-Since': 'Fri, 05 Oct 2018 09:34:44 GMT',
        }
        # self.ua=UserAgent()

        self.con = pymysql.Connect(host='127.0.0.1', user='root', password='root', port=3306, database='jobble')
        self.cursor = self.con.cursor()


    def download_parse(self,url_list):
        """下载解析"""
        for url in url_list:
            gevent.sleep(1.5)
            # self.headers['User-Agent'] = self.ua.random
            html = requests.get(url, headers=self.headers).text
            html = etree.HTML(html)
            comp=''.join(html.xpath('//*[@id="home"]/div/div[1]/div/div[2]/div[1]/span/h1/@data-fullname'))
            print(comp)
            #self.insert_mysql(comp)

    def insert_mysql(self,comp):
        """写入数据库"""
        sql = 'INSERT INTO juzi (comp) VALUES ({});'.format(comp)
        try:
            if self.cursor.execute(sql):
                self.con.commit()
                print('Successful')
        except Exception as e:
            print(e)
            print('Failed')

def start_geven(crawl,help,url_list):
    # 开启20个协程
    process_url_list =  help.task(url_list, 10)
    print(process_url_list)

    task_list = []
    for i in range(len(process_url_list)):
        gevent.sleep(2)
        task_list.append(gevent.spawn(crawl.download_parse, process_url_list[i]))
    gevent.joinall(task_list)

def start_thread(crawl,help,url_list):
    process_url_list = help.task(url_list,8)
    for i in range(len(process_url_list)):
        time.sleep(1)
        threading.Thread(target=start_geven, args=(crawl,help,process_url_list[i],)).start()


def get_id(cursor):
    sql="""select com_id from juzi;"""
    cursor.execute(sql)
    print('4')
    return cursor.fetchall()




if __name__ == '__main__':
    con = pymysql.Connect(host='127.0.0.1', user='root', password='root', port=3306, database='jobble')
    cursor = con.cursor()

    help=itjuzi_helper.Helper()
    id_list = get_id(cursor)
    url_list=help.gen_url(id_list)
    # process_url_list = help.task(url_list,3)

    crawl=CrawlCompDetail()
    start_thread(crawl,help,url_list,)
    # p=Pool(3)
    # print(p)
    # for i in range(len(process_url_list)):
    #     print(i)
    #     p.apply(pr.start_geven,args=(process_url_list[i],))
    #     print('开启进程池')
    # p.close()
    # p.join()
    # process_list=[]
    # for i in range(len(process_url_list)):
    #
    #     print(process_url_list[i])
    #     time.sleep(1)
    #     process=multiprocessing.Process(target=start_thread,args=(crawl,help,process_url_list[i],))
    #     process.start()
    #     print('开启进程池')
    #     process_list.append(process)
    #
    # for process in process_list:
    #     process.join()

    #con.close()














