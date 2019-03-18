# -*- coding: utf-8 -*-
__author__ = 'admin'
__date__ = '2018/7/3 19:03'

import hashlib


class Helper:

    def get_md5(self,url):
        # 判断url是不是unicode对象
        if isinstance(url,str):
            url=url.encode('utf-8')
        # 创建md5对象
        m=hashlib.md5()
        m.update(url)

        # python不能直接调用,因为不是unicode是str需要转成unicode才能加密
        return m.hexdigest()


