# -*- coding: utf-8 -*-
__author__ = 'admin'
__date__ = '2018/11/25 19:28'
import math


def generade_id():
    for id in range(2110001,3600000):
        yield id


def return_page(page_num):

    num= page_num / 3
    if not isinstance(num,int):
        return (math.floor( page_num / 3)+1)
    else:
        return (math.floor( page_num / 3))


def is_wining_num(num):
    if int(num) <= 4:
        return True





