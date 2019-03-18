import multiprocessing#分布式进程
import multiprocessing.managers#分布式进程管理器
import demjson
import os
import time
import requests



class QueueManger(multiprocessing.managers.BaseManager):
    """分布式管理器"""
    pass



def get_url():
    try:
        data=task.get(timeout=100)
        yield data
    except Exception as e:
        print(e)


def get_comment(comment_url,result):
    time.sleep(2)
    print('当前进程---->%s:'%os.getpid())

    res=requests.get(comment_url).text
    res = demjson.decode(res.strip()[11:-1])
    for comment in res['result']['comments']:
        info = {}
        info['guid'] = comment['guid']
        info['comment'] = comment['content']
        info['title'] = comment['referenceName']
        info['nickname'] = comment['nickname']
        info['size'] = comment['productSize']
        info['color'] = comment['productColor']
        info['level'] = comment['userLevelName']
        try:
            info['peizhi'] = comment['productSales'][0]['saleValue']
        except Exception as e:
            info['peizhi'] = comment['productSize']
        info['client'] = comment['userClientShow']
        print(info)
        result.put(info)





if __name__ == '__main__':
    QueueManger.register('get_task')  # 注册函数
    QueueManger.register('get_result')
    manger = QueueManger(address=('127.0.0.1', 8848), authkey='12345'.encode('utf-8'))
    manger.connect()  # 连接服务器
    task = manger.get_task()
    result = manger.get_result()
    flag=True
    processlist = []
    while flag:
        for i in range(1, 5):
            process = multiprocessing.Process(target=get_comment,args=(next(get_url()),result))
            process.start()
            processlist.append(process)
        for process in processlist:
            process.join()

        time.sleep(1)
        if task.empty():
            flag=False


