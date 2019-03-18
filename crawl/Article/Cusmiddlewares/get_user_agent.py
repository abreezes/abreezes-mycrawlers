# -*- coding: utf-8 -*-
__author__ = 'admin'
__date__ = '2018/7/25 19:52'
import logging
from fake_useragent import UserAgent

class RandomUserAgentMiddleware(object):
    def __init__(self):
        super(RandomUserAgentMiddleware,self).__init__()
        self.ua=UserAgent()

