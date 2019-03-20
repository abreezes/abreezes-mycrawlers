# -*- coding: utf-8 -*-
__author__ = 'admin'
__date__ = '2018/7/3 19:03'

import hashlib

def get_md5(id):
    # 判断url是不是unicode对象
    if isinstance(id,str):
        id=id.encode('utf-8')
    # 创建md5对象
    m=hashlib.md5()
    m.update(id)

    # python不能直接调用,因为不是unicode是str需要转成unicode才能加密
    return m.hexdigest()

# 加上if __name__ == '__main__',导到别的文件种种main以下的代码都不会运行
if __name__ == '__main__':
    print(get_md5('http://blog.jobble.com'))