# -*- coding: utf-8 -*-
import scrapy
import json

from utils import common
import time

from items import TianYanChaItemLoader,TianYanChaItem

class TianyanchaSpider(scrapy.Spider):
    name = 'tianyancha'
    allowed_domains = ['www.tianyancha.com','shamen.tianyancha.com']
    start_urls = ['https://shamen.tianyancha.com/search/p1']

    header = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        'Content-Type': 'application/json',
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "shamen.tianyancha.com",
        "Referer": "https://shamen.tianyancha.com/search",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest", }
    token=""


    def parse(self, response):
        compy_url=response.xpath("//div[@class='header']/a/@href").extract()
        for url in compy_url:
            if url:
                yield scrapy.Request(url=url,cookies={'auth_token':self.token},meta={'cookiejar':response.meta['cookiejar']},callback=self.parse_page,dont_filter=True)
        page_url=response.xpath("//div[@class]/ul/li[last()]/a/@href").extract_first()
        if page_url:
            yield  scrapy.Request(url=page_url,cookies={'auth_token':self.token},meta={'cookiejar':response.meta['cookiejar']},headers=self.header,callback=self.parse)

    def parse_page(self,response):
        # 使用自定义ArticleItemLoader

        item_loader=TianYanChaItemLoader(item=TianYanChaItem(),response=response)

        item_loader.add_xpath('compname',"//div[@class='header']/h1/text()")
        item_loader.add_xpath('phone',"//div[@class='detail ']/div[1]/div[1]/span[2]/text()|//div[@class='detail']/div[1]/div[1]/span[2]/text()")
        item_loader.add_xpath('email',"//div[@class='detail']/div/div[2]/span[@class='email']/text()")
        item_loader.add_value('url',response.url)
        item_loader.add_value('object_id',common.get_md5(response.url))
        # 法定代表人
        item_loader.add_xpath('fddb',"//div[@id='_container_baseInfo']/table/tbody/tr/td[1]/div[1]/div/div[2]/div/a/@title")
        # 注册资本
        item_loader.add_xpath('zczb',"//div[@id='_container_baseInfo']/table/tbody/tr/td[2]/div[2]/@title")
        # 注册时间
        item_loader.add_xpath('zctime',"//div[@id='_container_baseInfo']/table[1]/tbody/tr[2]/td[1]/div[2]/text/text()")
        # 公司状态
        item_loader.add_xpath('gszt',"//div[@id='_container_baseInfo']/table/tbody/tr[3]/td/div[2]/@title")
        # 工商id
        item_loader.add_xpath('gsid',"//div[@id='_container_baseInfo']/table[2]/tbody/tr[1]/td[2]/text()")
        # 组织机构id
        item_loader.add_xpath('orgid',"//div[@id='_container_baseInfo']/table[2]/tbody/tr[1]/td[4]/text()")
        # 信用id
        item_loader.add_xpath('xyid',"//div[@id='_container_baseInfo']/table[2]/tbody/tr[2]/td[2]/text()")
        # 公司类型
        item_loader.add_xpath('gstype',"//div[@id='_container_baseInfo']/table[2]/tbody/tr[2]/td[4]/text()")
        # 纳税人id
        item_loader.add_xpath('nsrid',"//div[@id='_container_baseInfo']/table[2]/tbody/tr[3]/td[2]/text()")
        # 行业
        item_loader.add_xpath('hy',"//div[@id='_container_baseInfo']/table[2]/tbody/tr[3]/td[4]/text()")
        # 营业期限
        item_loader.add_xpath('yyqx',"//div[@id='_container_baseInfo']/table[2]/tbody/tr[4]/td[2]/span/text()")
        # 核准日期
        item_loader.add_xpath('hzrq',"//div[@id='_container_baseInfo']/table[2]/tbody/tr[4]/td[4]/text/text()")
        # 公司规模
        item_loader.add_xpath('size',"//div[@id='_container_baseInfo']/table[2]/tbody/tr[5]/td[4]/text()")
        # 实缴资本
        item_loader.add_xpath('sjzb',"//div[@id='_container_baseInfo']/table[2]/tbody/tr[6]/td[2]/text()")
        # 登记机构
        item_loader.add_xpath('djjg',"//div[@id='_container_baseInfo']/table[2]/tbody/tr[6]/td[4]/text()")
        # 地址
        item_loader.add_xpath('addr',"//div[@id='_container_baseInfo']/table[2]/tbody/tr[8]/td[2]/text()")
        # 经营范围
        item_loader.add_xpath('jyfw',"//div[@id='_container_baseInfo']/table[2]/tbody/tr[9]/td[2]/span/span/span[1]/text()")
        # 高管姓名
        item_loader.add_xpath('zyry',"//div[@id='_container_staff']/div/table/tbody/tr/td/div/a[1]/text()")
        # 股东信息
        item_loader.add_xpath('gdxx',"//div[@id='_container_holder']/table/tbody/tr/td/div/div[2]/a/text()")

        tianyancha_item=item_loader.load_item()


        yield tianyancha_item


    def start_requests(self):
        base_url = 'https://www.tianyancha.com/login/'
        return [scrapy.Request(url=base_url,meta={'cookiejar':1},headers=self.header,callback=self.get_token)]


    def get_token(self,response):
        time.sleep(0.5)
        login_url = 'https://www.tianyancha.com/cd/login.json'
        form_data ={"mobile": "18554835078", "cdpassword": "37d066f9b52b1eff5f5a56ec36ca3869", "loginway": "PL",
                     "autoLogin": 'true'}
        return [scrapy.FormRequest(url=login_url,
                                   method='POST',
                                   body=json.dumps(form_data),
                                   meta={'cookiejar':response.meta['cookiejar']},
                                   headers=self.header,callback=self.tokens)]

    def tokens(self,response):
        time.sleep(0.5)
        self.token = (json.loads(response.text))['data']['token']

        index_url = 'https://www.tianyancha.com/usercenter/modifyInfo'
        return scrapy.Request(url=index_url,cookies={'auth_token':self.token},meta={'cookiejar':response.meta['cookiejar']},headers=self.header,callback=self.check_login)


    def check_login(self,response):

        index_url='https://www.tianyancha.com/usercenter/modifyInfo'
        if response.url == index_url:
            for url in self.start_urls:
                yield scrapy.Request(url,dont_filter=True,cookies={'auth_token':self.token},meta={'cookiejar':response.meta['cookiejar']},headers=self.header)








