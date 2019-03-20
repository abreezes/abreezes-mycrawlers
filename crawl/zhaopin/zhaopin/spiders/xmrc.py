# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import settings
from urllib.request import urljoin
from items import XmrcItem,XmrcItemLoader
from utils.common import get_md5
from utils.get_jobtype_addr import get_type
import time

class XmrcSpider(scrapy.Spider):
    name = 'xmrc'
    allowed_domains = ['xmrc.com.cn']
    start_urls = ['https://www.xmrc.com.cn']
    base_url='https://www.xmrc.com.cn'


    def __init__(self):
        self.key_words = settings.KeyWords
        self.page_num = 10
        self.base_start_url=settings.XMRC_START_URL
        self.pop_key = settings.POP_KEY

    def parse(self, response):
        # urls, zhuanye =next(self.genCrawlUrl())
        # print(urls,zhuanye)
        for urls,zhuanye in self.genCrawlUrl():
            for url in urls:
                yield Request(url=url, meta={'zhuanye':zhuanye},dont_filter=True,callback=self.get_detail_url)

    def get_detail_url(self, response):
        """获取职位详情"""
        zhuanye=response.meta.get('zhuanye')
        url_list=response.xpath('//*[@id="ctl00$Body$JobRepeaterPro_main_div"]/table[2]/tr/td[2]/a/@href').extract()
        title_elm = response.xpath("//*[@id='ctl00$Body$JobRepeaterPro_main_div']/table[2]/tr/td[2]/a")
        # 去除多余的节点
        titles_list = [i for i in title_elm if '实习' or '兼职' not in i.xpath('string(.)').strip()]
        for url,title_info in zip(url_list,titles_list):
            title=title_info.xpath('string(.)').extract_first().strip()
            # 无关职位链接不进行采集
            if self.pop_key[0] not in title and self.pop_key[1] not in title and self.pop_key[2] not in title and \
                            self.pop_key[3] not in title:
                # 岗位类型
                job_type=get_type(title)
                yield Request(url=self.base_url+url,meta={'zhuanye':zhuanye,'job_type':job_type,
                                                  'JsPage':False},callback=self.parse_detail)
            else:
                continue
    def parse_detail(self,response):
        item_loader = XmrcItemLoader(item=XmrcItem(), response=response)
        item_loader.add_value('zhuanye',response.meta.get('zhuanye'))
        item_loader.add_value('job_type',response.meta.get('job_type'))
        item_loader.add_value('object_id',get_md5(response.url))
        item_loader.add_value('link',response.url)
        item_loader.add_value('addr','厦门')
        item_loader.add_value('select_time',time.strftime(settings.TIME_SELECT_FORMAT))
        item_loader.add_value('crawl_name',self.name)
        item_loader.add_value('crawl_time',time.strftime(settings.SQL_DATE_FORMAT))
        item_loader.add_value('ident',settings.IDENT)
        item_loader.add_value('company_type','')
        item_loader.add_value('company_size','')
        item_loader.add_value('company_industry','')
        item_loader.add_xpath('title','//tr[1]/td/font[1]/a/u/text()')
        item_loader.add_xpath('company_name','//*[@id="container"]/table[2]/tr/td[3]/table[4]/tr[1]/td[2]/table[1]/tr[2]/td[2]/table/tr/td[contains(text(),"招聘单位")]/text()')
        item_loader.add_xpath('salarys','//tr[1]/td[2]/table[1]/tr[last()-3]/td/table/tr/td[contains(text(),"参考月薪")]/text()')
        item_loader.add_xpath('experience','//tr[1]/td[2]/table[1]/tr[last()-3]/td/table/tr/td[contains(text(),"招聘对象")]/text()')
        item_loader.add_xpath('education','//tr[1]/td[2]/table[1]/tr[last()-3]/td/table/tr/td[contains(text(),"学历要求")]/text()')
        item_loader.add_xpath('job_nums','//tr[1]/td/font[1]/font/b/text()')
        item_loader.add_xpath('job_desc','//*[@id="container"]/table[2]/tr/td[3]/table[4]/tr[1]/td[2]/table[1]/tr[last()-1]/td[2]/text()')
        item_loader.add_xpath('company_addr','//*[@id="ctl00_Body_Repeater1_ctl00_ctl02_Repeater1_ctl00_ctl03_ctl00_Tr2"]/td[2]/text()')
        item_loader.add_xpath('phone',"//tr[@id='ctl00_Body_Repeater1_ctl00_ctl02_Repeater1_ctl00_ctl03_ctl00_Tr1']/following-sibling::*[1]/td[2]/text()")
        item_loader.add_xpath('contact','//*[@id="ctl00_Body_Repeater1_ctl00_ctl02_Repeater1_ctl00_ctl03_ctl00_Tr1"]/td[2]/text()')
        item_loader.add_xpath('release_time','//*[@id="container"]/table[2]/tr/td[3]/table[4]/tr[1]/td[2]/table[1]/tr/td[contains(text(),"招聘期限")]/text()')
        item_loader.add_xpath('max_salary','//tr[1]/td[2]/table[1]/tr[last()-3]/td/table/tr/td[contains(text(),"参考月薪")]/text()')
        item_loader.add_xpath('min_salary','//tr[1]/td[2]/table[1]/tr[last()-3]/td/table/tr/td[contains(text(),"参考月薪")]/text()')

        yield item_loader.load_item()

    def genCrawlUrl(self):
        # 生成start_url
        for key in self.key_words.keys():
            for words in self.key_words.get(key):
                start_url = [self.base_start_url.format(words,page) for page in range(1, self.page_num)]
                yield (start_url,key)