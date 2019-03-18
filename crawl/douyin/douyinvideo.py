# -*- coding: utf-8 -*-
from gevent import monkey;monkey.patch_all()
import gevent
import re
import time
from selenium import webdriver
import requests
from urllib import request



class DouYinVideo:
    headers = {
        'cookie': '_ba=BA0.2-20190127-5199e-kW9UQE6z2jGEFCL5GaGN; _ga=GA1.2.1922202211.1550149902; _gid=GA1.2.357055306.1550149902',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        'accept': 'application/json',
        # 'referer': 'https://www.douyin.com/share/user/{}'.format(share_id),
        'authority': 'www.douyin.com',
        'x-requested-with': 'XMLHttpRequest',
    }
    with open('./douyin_hot_id.txt','r') as f:
        hot_id_list=f.readlines()

    def get_singtrue(self,share_id):
        """获取singtrue的值"""
        share_url = 'https://douyin.com/share/user/{}'.format(share_id)
        response = requests.get(url=share_url, headers=self.headers)
        dytk_search = re.compile(r"dytk: '(.*?)'")
        tac_search = re.compile(r'<script>tac=(.*?)</script>')
        dytk = re.search(dytk_search, response.text).group(1)
        tac = 'var tac=' + re.search(tac_search, response.text).group(1) + ';'

        with open('head.txt', 'r') as f1:
            f1_read = f1.read()

        with open('foot.txt', 'r') as f2:
            f2_read = f2.read().replace('&&&', share_id)
            f3_read = f2_read.replace("**tac", tac)

        with open('./head.html', 'w') as f_w:
            f_w.write(f1_read + '\n' + f3_read)

        driver=webdriver.Chrome(r'C:\Python36\chromedriver.exe')
        driver.get(r'E:\python\sc\douyin\head.html')
        sign=driver.title
        driver.quit()

        return sign,dytk

    def get_video_url(self,share_id,sign,dytk):
        """获取videourl"""
        url='https://www.douyin.com/aweme/v1/aweme/post/?user_id={share_id}&count=21&max_cursor=0&aid=1128&_signature={sign}&dytk={dytk}'.format(share_id=share_id,sign=sign,dytk=dytk)
        response=requests.get(url=url,headers=self.headers).json()
        url_list=[]
        if response['aweme_list']:
            for url in response['aweme_list']:
                url_list.append({'{}'.format(url['aweme_id']):'{}'.format(url['video']['play_addr']['url_list'][0])})
                # url_list.append(url['video']['play_addr']['url_list'][0])
            return url_list

    def download_video(self,url_list,share_id):
        # 下载video
        for url in url_list:
            for id,url in url.items():
                print('正在下载:{}-{}'.format(share_id,id))
                response=requests.get(url,headers=self.headers).content
                with open('./video/{}-{}.mp4'.format(share_id,id),'wb') as f:
                    f.write(response)

    def main(self):
        for share_id in self.hot_id_list:
            share_id=share_id.strip()
            if share_id:
                sign, dytk=self.get_singtrue(share_id)
                url_list=self.get_video_url(share_id,sign,dytk)

                xclist = [[], [], [], [], []]
                n = len(xclist)
                for i in range(len(url_list)):
                    xclist[i % n].append(url_list[i])
                task_list = []
                for i in range(n):
                    task_list.append(gevent.spawn(self.download_video, xclist[i],share_id))

                gevent.joinall(task_list)
        else:
            print('全部下载完成')



if __name__ == '__main__':
    douyin=DouYinVideo()
    douyin.main()
    end=time.time()




