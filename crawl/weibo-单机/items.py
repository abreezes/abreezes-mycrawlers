# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    prize_name=scrapy.Field()
    prize_num=scrapy.Field()
    prize_type=scrapy.Field()
    pageid=scrapy.Field()
    rule=scrapy.Field()
    wb_id=scrapy.Field()
    created_at = scrapy.Field()
    attitudes_count = scrapy.Field()
    comments_count = scrapy.Field()
    reposts_count = scrapy.Field()
    text = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    #
    # def get_insert_sql(self):
    #     return insert(self,'weiboprize')




class WeiboUserItem(scrapy.Item):
    # 是否是中奖用户
    is_winner_user=scrapy.Field()
    user_id=scrapy.Field()
    nick=scrapy.Field()
    wb_id = scrapy.Field()
    wb_count=scrapy.Field()
    # 粉丝数
    followers_count=scrapy.Field()
    # 关注数
    follow_count=scrapy.Field()
    # 微博等级
    wb_lv=scrapy.Field()
    #注册时间
    created_at = scrapy.Field()
    #信用等级
    credit_lv=scrapy.Field()
    gender=scrapy.Field()
    #是否认证
    is_verify=scrapy.Field()
    # 用户类型(企业/个人账号)
    user_type=scrapy.Field()


    # def get_insert_sql(self):
    #     return insert(self,'weibouser')


def insert(value,table):
    """生成sql语句"""
    table = table
    keys = ','.join(value.keys())
    values = ','.join(['%s', ] * len(value))

    insert_sql = """INSERT INTO {table}({keys})""".format(
        table=table, keys=keys, values=values)

    params = tuple(value.values())
    return insert_sql, params
