from gevent import monkey;monkey.patch_all()
import gevent
import threading
import multiprocessing
import requests
import os
import re

from contextlib import closing

class MuKe:
    headers = {
        "Host":"www.icourse163.org",
        "Accept":"*/*",
        "device-id":"375E84B2-E93D-4551-8D8A-33B0D770B936",
        "edu-app-version":"3.9.2",
        "Accept-Encoding":"br, gzip, deflate",
        "Accept-Language":"zh-Hans-CN;q=1",
        "event-distinct-id":"7bcd6dd451e8e857dfa5488e32944dff",
        "edu-app-type":"iPhone",
        "edu-unique-id":"{'id_ver': 'IOS_1.0.3','rk': 'VJMsaUK9v9GxsFL+SIiMmvm2tV99S\/K+fPGUQvwTosXpE\/udmiwwTtkteBg9eb33kxHMQ2nSnyMiHjZVKCXXk8U7bDGdSmryofiws3WCNsGRVnRk8QzmfgPQCJjVa6xV8Q55pKR1JQ+rFWzuegKmYQXsKGl4yaaIUCXhFiAxrNk=','rdata': '5lHqegTvlTnev1d8PvJNtgPSbAbrMRiuKSB8SB4\/VnhGCLzJhHyHhQINNvw1FJ0h','datatype':'aimt_datas'}",
        "User-Agent":"edumooc/3.9.2 (iPhone; iOS 12.1; Scale/2.00)",
        "Content-Length":"420",
        "Connection":"keep-alive",
        "Content-Type":"application/x-www-form-urlencoded",
        "Cookie":"WM_NI=Y0ZYDoqPUeozk79y1GgSdaKuMsfNboFaG0XhyCXJN2nNxP05Ec0w0ijMlwDiwgp6vMFnOLWfewTD6efdur6F5PYkTIb0%2B%2FSOO9PmXx%2Fil4unSn5XE3nCD28nGQRZGVMcMVA%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee87cc59bce99ab0f467bc868ab2d14f938f8abab87da2aca1d1cc61ed8c81b6d22af0fea7c3b92a9bf096bac765b3909b86ee72a9e9f79ab44da58dac82ca7f8fadaaafe16586bf89d1db64bb9d98abcd3aae92b8b1b33f87bd0098b363aa93a498c763b5b9c0d7f54786b281add66ea7a99ca5b56fa6bcbb93b54ef790978cd743a2f0e5d0d2458de7a08edb74edb7a4d5f86691b2fbb9c839ae9d8cd3bb66858f9ebbc65e8fbd83b7c437e2a3; WM_TID=ZMQrkL5B5t5AEUBUEAd5xPptxdlqTPAG; __utma=63145271.819446279.1550324494.1550324494.1550324494.1; __utmz=63145271.1550324494.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); EDUWEBDEVICE=5c19190f2da540278af33d86caabbd21",

    }
    base_dir='./video'
    dir_reg=re.compile(r'[*|\\|/|:|*|"|<|>|\|]')
    def __init__(self):
        try:
            os.mkdir(self.base_dir)
        except FileExistsError:
            pass

    def get_video_url(self,cid=None,tid=None):

        data={
            "cid":"{}".format(cid),
            "mob-token":"1cfe88a17139b892a7ea968d20ede492d70c0a036f4fa93b2f801e4c6dd6f56bce3db354ef0194f7b6512da59aa550075f775b38d87eca24ffd72424c7cc8b97247899af117406af9e5bb8cfa5021d093fe82d8881bd18d30e2ebd9980e23f4b0d7ef1ee30366d043e17db84286433cef4003c06966b5adc975c6501a511b4335a3e8a4dd70593bb5ac7961e77e891c63f33b9199ac98710eb4242d44ea0b2a78676b27e0d374f2f0db184284eeb568ef068144cfcbaf5b449620a83b20dcbf5",
            'tid':"{}".format(tid),
        }

        url = 'https://www.icourse163.org/mob/course/courseLearn/v2'
        response = requests.post(url, headers=self.headers, data=data).json()
        url_list=[]
        # 课程目录
        course_dir=self.base_dir+ '/' + response['results']['courseDto']['name']+'--'+response['results']['courseDto']['schoolName']
        # 章
        for chapter in response['results']['termDto']['chapters']:
            # 章目录
            chapter_dir_name=chapter['name']
            # 节目录
            for lesson in chapter['lessons']:
                dir_name=course_dir+'/'+re.sub(self.dir_reg,'-',chapter_dir_name)+'/'+re.sub(self.dir_reg,'-',lesson['name'])
                try:
                    os.makedirs(dir_name,exist_ok=True)
                except FileExistsError:
                    pass

                # 资源video
                for unit in lesson['units']:
                    if unit['contentType'] == 1:
                        name = dir_name+'/'+re.sub(self.dir_reg,'',unit['name'])+'.mp4'
                        url_list.append({'name':'{}'.format(name),'url':'{}'.format(unit['resourceInfo']['videoUrl'])})
                    elif unit['contentType'] == 3:
                        name = dir_name + '/' + re.sub(self.dir_reg, '', unit['name']) + '.pdf'
                        url_list.append({'name':'{}'.format(name),'url':'{}'.format(unit['resourceInfo']['textUrl'])})

        return url_list

    def download(self,url_list):
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"}
        for url in url_list:
            name=url['name'][url['name'].rfind('/')+1:]
            print(name)
            with closing(requests.get(url=url['url'],headers=headers,stream=True)) as response:
                chunk_size = 1024  # 单次请求最大值
                content_size = int(response.headers['content-length'])  # 内容体总大小
                progress = ProgressBar(name, total=content_size,
                                       unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")

                with open(url['name'],'wb') as f:
                    for data in response.iter_content():
                        f.write(data)
                        progress.refresh(count=len(data))

    def task_cut(self,url_list,num=5):
        """任务切割"""
        xclist = [[] for i in range(num)]
        n = len(xclist)
        for i in range(len(url_list)):
            xclist[i % n].append(url_list[i])
        return xclist

    def start_thread(self,url_list):
        #线程
        task_list=[]
        xclist=self.task_cut(url_list,num=3)
        n=len(xclist)
        for i in range(n):
            mythread = threading.Thread(target=self.start_xc, args=(xclist[i],))
            mythread.start()
            task_list.append(mythread)
        for thd in task_list:
            thd.join()

    def start_xc(self,url_list):
        """协程"""
        xclist=self.task_cut(url_list)
        task_list = []
        for i in range(len(xclist)):
            task_list.append(gevent.spawn(self.download, xclist[i],))
        gevent.joinall(task_list)


    def main(self,cid,tid):
        url_list = self.get_video_url(cid,tid)
        xclist=self.task_cut(url_list,num=3)
        task_list = []
        for i in range(len(xclist)):
            process = multiprocessing.Process(target=self.start_thread, args=(xclist[i],))
            process.start()
            task_list.append(process)  # 开启多进程

        for p in task_list:
            p.join()

    def  searcher_course(self,key,stats=0):
        """课程搜索"""
        # 即将开始20 正在进行10 全部30 结束0
        url='https://www.icourse163.org/mob/course/search/v1'
        data={"courseTagType":"0",
                "highlight":"true",
                "keyword":key,
                "mob-token":"1cfe88a17139b892a7ea968d20ede492d70c0a036f4fa93b2f801e4c6dd6f56bce3db354ef0194f7b6512da59aa550075f775b38d87eca24ffd72424c7cc8b97247899af117406af9e5bb8cfa5021d093fe82d8881bd18d30e2ebd9980e23f4b0d7ef1ee30366d043e17db84286433cef4003c06966b5adc975c6501a511b4335a3e8a4dd70593bb5ac7961e77e891c63f33b9199ac98710eb4242d44ea0b2a78676b27e0d374f2f0db184284eeb568ef068144cfcbaf5b449620a83b20dcbf5",
                "orderBy":"0",
                "p":"1",
                "psize":"20",
                "stats":stats,}

        response=requests.post(url=url,data=data,headers=self.headers).json()
        course_list=[]
        for obj in response['results']['result']:
            school=obj['highlightUniversity']
            teacher=obj['highlightTeacherNames']
            name= obj['mocCourseCardDto']['name']
            cid=obj['cid']
            tid=obj['mocCourseCardDto']['currentTermId']
            course_list.append({'cid':cid,'tid':tid,'school':school,'name':name,'teacher':teacher})
        return course_list

    def print_info(self):
        key = input('输入搜索的关键词:')
        for i, stats in enumerate(['全部', '正在进行', '即将开课', '已结束']):
            print('{}'.format(i) + '\t' + stats + '\t' + '\n')
        num = int(input('选择课程状态:'))
        if num == 0:
            num = 30
        elif num == 1:
            num = 10
        elif num == 2:
            num = 20
        elif num == 3:
            num = 0
        else:
            print('输入有误')
        return key,num

class ProgressBar:

    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "【%s】%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)

if __name__ == '__main__':
    # MuKe().main()
    key,num=MuKe().print_info()
    course_list=MuKe().searcher_course(key,num)
    print('序号'+'\t'+'课程名程'+'\t'+'学校'+'\t'+'教师'+'\n')
    for i,course in enumerate(course_list):
        print('{}'.format(i)+'\t'+'{}'.format(course['name'])+'\t'+
              '{}'.format(course['school'])+'\t'+'{}'.format(course['teacher'])+'\n')
    num=int(input('选择要下载的课程:'))
    course=course_list[num]
    print(course['cid'],course['tid'])
    MuKe().main(course['cid'],course['tid'])






