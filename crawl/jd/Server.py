import hashlib
import multiprocessing#分布式进程
import multiprocessing.managers#分布式进程管理器
import random,time,re
from multiprocessing import Queue
import downloads
import getskuid
import helper
import pymongo
import parses



class QueueManger(multiprocessing.managers.BaseManager):
    """分布式管理器,继承,进程间共享数据"""
    pass


class GetCommentURL:
    """获取评论url"""

    def __init__(self):
        self.num_count=0

        self.download=downloads.Downlaod()

        self.getskuid=getskuid.GetSKUId()

        self.gen_md5=helper.Helper()

        self.base_comment_url = 'http://wq.jd.com/commodity/comment/getcommentlist?sorttype=5&sceneval=2&sku={}&page=1&pagesize=10&score=0&callback=skuJDEvalB&t=0.225512337012296'

        self.parse=parses.Parse('get_comment_page')

    @property
    def comment_url(self):
        """爬取的初始连接用于获取每个skuid的总页数 即每个skuid的第一页"""
        for id in self.getskuid.get_skuid:
            url = self.base_comment_url.format(id)
            yield url

    @property
    def get_comment_page(self):
        """获取总页数"""
        for url in self.comment_url:
            html=self.download.download(url)
            comments_page=self.parse.parses(html)
            yield comments_page['result']['maxPage'], url

    @property
    def gen_comment_urls(self):
        """生成要爬取的url 即每个skuid评论的所有链接"""
        for pages, url in self.get_comment_page:
            url = re.sub('page=(\d+)?&', 'page={}&', url)
            for page in range(1, pages):
                yield url.format(page)


task_queue = Queue()  # 任务队列
result_queue = Queue()  # 结果队列


def return_task():
    """返回任务队列"""
    return task_queue


def return_result():
    """返回结果队列"""
    return result_queue


def get_result(result):
    """获取结果"""
    res = result.get(timeout=100)
    yield res


def get_url(comment_url,task):
    """压入任务"""
    for url in comment_url.gen_comment_urls:
        print(url)
        task.put(url)

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
collection = client.project.jd

def write_mango(result):
    for res in get_result(result):
        collection.insert(res)
        print(' Success', res)


if  __name__ == '__main__':

    comment_url = GetCommentURL()

    multiprocessing.freeze_support()
    QueueManger.register('get_task', callable=return_task)
    QueueManger.register('get_result', callable=return_result)

    manger = QueueManger(address=('127.0.0.1', 8848), authkey='12345'.encode('utf-8'))
    manger.start()  # 开启
    task = manger.get_task()
    result = manger.get_result()
    task.put(next(comment_url.gen_comment_urls))

    flag=True
    while flag:
        processlist = []
        time.sleep(1.5)
        if not task.empty():
            for i in range(1,3):
                task_process = multiprocessing.Process(target=get_url, args=(comment_url,task,))
                task_process.start()
                processlist.append(task_process)

        time.sleep(1.5)
        if not result.empty():
            for i in range(1, 4):
                process = multiprocessing.Process(target=write_mango, args=(result,))
                process.start()
                processlist.append(process)
        else:
            flag = False

        for process in processlist:
            process.join()

    manger.shutdown()


