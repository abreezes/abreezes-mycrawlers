# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import settings
from items import WuYouItem,WuYouItemLoader
from utils.common import get_md5
from utils.get_jobtype_addr import get_type,get_addr
import time
import datetime


class ZhilianSpider(scrapy.Spider):
    name = 'qcwy'
    allowed_domains = ['51job.com']
    start_urls = ['https://www.51job.com']
    #base_url='https://www.xmrc.com.cn'
    custom_settings = {

    }

    def __init__(self):
        self.key_words = settings.KeyWords
        self.page_num = settings.PageMax
        self.base_start_url=settings.WY_START_URL
        self.code=settings.WY_ADDR_CODE
        self.pop_key=settings.POP_KEY
        print(self.pop_key)

    def parse(self, response):
        #urls, zhuanye = next(self.genCrawlUrl())
        for urls,zhuanye in self.genCrawlUrl():
            for url in urls:
                addr=get_addr(url)
                yield Request(url=url, meta={'zhuanye':zhuanye,'addr':addr}, dont_filter=True,callback=self.get_detail_url)

    def get_detail_url(self, response):
        """获取职位详情"""
        zhuanye=response.meta.get('zhuanye')
        addr=response.meta.get('addr')

        url_list=response.xpath('//*[@id="resultList"]/div/p/span/a/@href').extract()
        title_list = response.xpath('//*[@id="resultList"]/div/p/span/a/@title').extract()
        salary_elm=response.xpath('//*[@id="resultList"]/div[@class="el"]/span[3]')
        release_time_list=response.xpath('//*[@id="resultList"]/div[@class="el"]/span[4]/text()').extract()

        for url,title,salary_info,release_time in zip(url_list,title_list,salary_elm,release_time_list):
            salary=salary_info.xpath('./text()').extract_first()
            if salary is None:
                salary='不限'

            for key in self.key_words[zhuanye]:
                if key in title and self.pop_key[0] not in title and self.pop_key[1] not in title and self.pop_key[2]\
                        not in title and self.pop_key[3] not in title and '元/天' not in salary:

                    # 岗位类型
                    job_type=get_type(title)
                    release_time=str(datetime.datetime.today().year)+'-'+release_time
                    yield Request(url=url,meta={'zhuanye':zhuanye,'job_type':job_type,
                                                'title':title,'salarys':salary,
                                                'addr':addr,'release_time':release_time},
                                  callback=self.parse_detail)
                else:
                    continue

    def parse_detail(self,response):
        item_loader = WuYouItemLoader(item=WuYouItem(), response=response)
        item_loader.add_value('zhuanye',response.meta.get('zhuanye'))
        item_loader.add_value('job_type',response.meta.get('job_type'))
        item_loader.add_value('object_id',get_md5(response.url))
        item_loader.add_value('link',response.url)
        item_loader.add_value('addr',response.meta.get('addr'))
        item_loader.add_value('salarys',response.meta.get('salarys'))
        item_loader.add_value('max_salary',response.meta.get('salarys'))
        item_loader.add_value('min_salary',response.meta.get('salarys'))
        item_loader.add_value('title',response.meta.get('title'))
        item_loader.add_value('release_time',response.meta.get('release_time'))
        item_loader.add_value('select_time',time.strftime(settings.TIME_SELECT_FORMAT))
        item_loader.add_value('crawl_name',self.name)
        item_loader.add_value('crawl_time',time.strftime(settings.SQL_DATE_FORMAT))
        item_loader.add_value('ident',settings.IDENT)
        item_loader.add_value('phone','')
        item_loader.add_value('contact','')
        item_loader.add_xpath('company_name','/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a/@title')
        item_loader.add_xpath('company_addr',"//div[@class='bmsg inbox']/p[@class='fp']/text()")
        item_loader.add_xpath('company_type','/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[1]/@title')
        item_loader.add_xpath('company_size','/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[2]/@title')
        item_loader.add_xpath('company_industry','/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[3]/@title')
        item_loader.add_xpath('experience','/html/body/div[3]/div[2]/div[2]/div/div[1]/p/@title')
        item_loader.add_xpath('education','/html/body/div[3]/div[2]/div[2]/div/div[1]/p/@title')
        item_loader.add_xpath('job_nums','/html/body/div[3]/div[2]/div[2]/div/div[1]/p/@title')
        item_loader.add_xpath('job_desc',"//div[@class='bmsg job_msg inbox']/p/text() | //div[@class='bmsg job_msg inbox']/p[2]/span/text() | //div[@class='bmsg job_msg inbox']/text()")


        yield item_loader.load_item()

    def genCrawlUrl(self):
        # 生成start_url
        for key in self.key_words.keys():
            for words in self.key_words.get(key):
                start_url = [self.base_start_url.format(code,words,page) for page in range(1, self.page_num) for code in self.code]
                yield start_url,key