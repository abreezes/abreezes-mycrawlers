# -*- coding: utf-8 -*-
import logging

from scrapy_redis.spiders import RedisSpider
import scrapy
from scrapy.log import logger

from weibo.wb_utils import utils
import demjson

from weibo.items import WeiboItem,WeiboUserItem
import re


class WeiboSpider(RedisSpider):
    name = 'Weibo'
    allowed_domains = ['weibo.com','m.weibo.cn','event.weibo.com']
    wining_url = 'https://event.weibo.com/yae/aj/event/mlottery/result?id={}&pageid='
    wining_url_pc = 'https://event.weibo.com/yae/aj/event/lottery/result?pageid={}&id={}&page={}&prizeLevel=1&_t=0'
    # start_urls = [wining_url]
    redis_key = 'Weibo:start_urls'
    home_page_url="https://m.weibo.cn/api/container/getIndex?type=uid&value={}&containerid=100505{}"
    user_base_url="https://m.weibo.cn/api/container/getIndex?containerid=230283{}_-_INFO&title=%E5%9F%BA%E6%9C%AC%E8%B5%84%E6%96%99&luicode=10000011&lfid=230283{}"

    referer_url='http://event.weibo.com/yae/event/lottery/result?pageid=&id={}&f=weibo'


    # 初始化
    def __init__(self,*args,**kwargs):
        super(WeiboSpider,self).__init__(*args,**kwargs)
        # logger = logging.getLogger('scrapy.spidermiddlewares.httperror')
        # logger.setLevel(logging.WARNING)
        self.generade_id=utils.generade_id()


    def parse(self, response):
        """解析抽奖平台"""
        response =demjson.decode(response.text)

        if response['code'] == '100000' and response['msg'] == 'ok':

            res = response['data']

            def return_prize_info(response):
                return response['prizeInfo'][0]

            def return_lottery_info(response):
                return response['lotteryInfo']

            def return_weibo_info(response):
                return response['weiboInfo']

            def return_winning_info(response,id):
                return response['winnerList'][id]

            item=WeiboItem()

            item['prize_name'] = return_prize_info(res).get('name')

            prize_num=return_prize_info(res).get('num')
            item['prize_num'] = prize_num
            item['prize_type'] = return_prize_info(res).get('type')
            pageid=return_lottery_info(res).get('pageid')
            item['pageid'] = pageid
            wb_id=return_lottery_info(res).get('id')
            item['wb_id']=wb_id
            item['rule'] = return_lottery_info(res)['rule'][0]

            item['created_at'] = return_weibo_info(res).get('created_at')
            item['attitudes_count'] = return_weibo_info(res).get('attitudes_count')
            item['comments_count'] = return_weibo_info(res).get('comments_count')
            item['reposts_count'] = return_weibo_info(res).get('reposts_count')
            item['text'] = return_weibo_info(res).get('text')
            user_id=return_weibo_info(res)['user'].get('id')
            item['user_id'] = user_id
            item['user_name'] = return_weibo_info(res)['user'].get('name')


            yield item

            # 奖品数量小于等于4的请求用户主页
            if utils.is_wining_num(prize_num):
                for i in range(0,int(prize_num)):

                    winner=return_winning_info(res,i)
                # for winner in return_winning_info(response):
                    winner_uid=winner['uid']
                    yield scrapy.Request(url=self.home_page_url.format(winner_uid,winner_uid),
                                         meta={'wb_id':wb_id,'is_winner_user':'1'},callback=self.parse_user_home,dont_filter=True)
            # 奖品数量大于4的
            else:
                pages=utils.return_page(int(prize_num))
                # self.headers['Host'] = 'event.weibo.com'
                for page in range(1,pages+1):
                    yield scrapy.Request(url=self.wining_url_pc.format(pageid,wb_id,page),meta={'wb_id':wb_id},
                                         callback=self.parse_pages_winner)

            # 抓取发起活动用户信息
            yield scrapy.Request(url=self.home_page_url.format(user_id,user_id),meta={'is_winner_user':0,'wb_id':wb_id},
                                 callback=self.parse_user_home,dont_filter=True)

        try:
            wb_id=self.generade_id.__next__()
            yield scrapy.Request(url=self.wining_url.format(wb_id), callback=self.parse)
        except Exception as e:
            pass
            # scrapy.Spider.close(self,'wb_id 为空')


    def parse_pages_winner(self,response):
        """解析获奖用户超过4个的页面"""
        res=demjson.decode(response.text)
        if res['code'] == '100000' and res['msg'] == 'ok':
            wb_id=response.meta.get('wb_id','None')

            html_str=res['data']['html']

            user_id_list=list(set(re.findall(r'.weibo.com/(\d+)/profile', html_str)))
            for id in user_id_list:
                yield scrapy.Request(url=self.home_page_url.format(id,id),meta={'wb_id':wb_id,'is_winner_user':'1'},callback=self.parse_user_home,dont_filter=True)

        try:
            wb_id=self.generade_id.__next__()
            yield scrapy.Request(url=self.wining_url.format(wb_id), callback=self.parse)
        except Exception as e:
            pass
            # scrapy.Spider.close(self,'wb_id 为空')



    def parse_user_home(self,response):
        """解析中奖者主页信息"""
        res=demjson.decode(response.text)
        if res['ok'] == 1:
            is_winner_user=response.meta.get('is_winner_user')
            wb_id=response.meta.get('wb_id','None')

            response = res['data']['userInfo']
            user_id = response.get('id')
            wb_count=response.get('statuses_count')
            followers_count = response.get('followers_count')
            follow_count = response.get('follow_count')
            gender=response.get('gender')


            yield scrapy.Request(url=self.user_base_url.format(user_id,user_id),
                                 meta={'is_winner_user':is_winner_user,'wb_id':wb_id,'user_id':user_id,'gender':gender,
                                       'wb_count':wb_count,'follow_count':follow_count,'followers_count':followers_count}
                                        ,callback=self.parse_user_base,dont_filter=True)

        try:
            wb_id = self.generade_id.__next__()
            yield scrapy.Request(url=self.wining_url.format(wb_id), callback=self.parse)
        except Exception as e:
            pass
            # scrapy.Spider.close(self, 'wb_id 为空')

    def parse_user_base(self,response):
        """解析用户基本资料"""
        res=demjson.decode(response.text)
        if res['ok'] == 1:
            item=WeiboUserItem()
            # 是否是中奖用户
            item['is_winner_user']=response.meta.get('is_winner_user')
            item['wb_id']=response.meta.get('wb_id')
            item['user_id']=response.meta.get('user_id')
            item['gender']=response.meta.get('gender')
            item['wb_count']=response.meta.get('wb_count')
            item['follow_count']=response.meta.get('follow_count')
            item['followers_count']=response.meta.get('followers_count')

            result=res['data']['cards']
            user_res = result[0]['card_group']
            if result[1]['card_group'][0]['desc'] == '个人信息':
            # if res[len(res)-3].get('item_name') == '等级' and res[len(res)-2].get('item_name') == '注册时间' and res[len(res)-1].get('item_name') == '阳光信用':
                # 个人用户
                item['nick']=user_res[1].get('item_content',None)
                item['wb_lv']= user_res[len(user_res)-3].get('item_content',None)
                item['created_at'] = user_res[len(user_res)-2].get('item_content',None)
                item['credit_lv'] = user_res[len(user_res)-1].get('item_content',None)
                item['user_type'] = 1
                if user_res[len(user_res)-5].get('item_type'):
                    item['is_verify']=1
                else:
                    item['is_verify']=0
            else:
                #企业用户
                item['nick']=user_res[1].get('item_content','None')
                item['wb_lv']= None
                item['created_at'] = None
                item['credit_lv'] = None
                item['user_type'] = 0
                if user_res[2].get('item_type'):
                    item['is_verify']=1
                else:
                    item['is_verify']=0

            yield item


            #     logger.info('parse_user_base function called on %s:%s',e,response.url)


    # def start_requests(self):
    #     yield scrapy.Request(url=self.wining_url.format(2110000),callback=self.parse)









