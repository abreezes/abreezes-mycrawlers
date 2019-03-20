# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import settings
from items import ZhiLianItem,ZhiLianItemLoader
from utils.common import get_md5
from utils.get_jobtype_addr import get_type,get_addr
import time
import demjson


class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    start_urls = ['https://www.zhaopin.com/']


    def __init__(self):
        self.key_words = settings.KeyWords
        self.page_num = settings.PageMax
        self.base_start_url=settings.ZL_START_URL
        self.code=settings.ZL_ADDR_CODE
        self.pop_key = settings.POP_KEY

    def parse(self, response):
        #urls, zhuanye = next(self.genCrawlUrl())
        for urls,zhuanye in self.genCrawlUrl():
            for url in urls:
                addr=get_addr(url)
                yield Request(url=url, meta={'zhuanye':zhuanye,'addr':addr}, dont_filter=True,callback=self.get_detail_url)

    def get_detail_url(self, response):
        """获取职位"""
        zhuanye=response.meta.get('zhuanye')
        addr=response.meta.get('addr')
        results=demjson.decode(response.text)['data']['results']
        for res in results:
            title=res.get('jobName','')
            company_name=res.get('company').get('name','')
            company_size=res.get('company').get('size').get('name','')
            company_type=res.get('company').get('type').get('name','')
            url=res.get('positionURL','')
            experience=res.get('workingExp').get('name','')
            education=res.get('eduLevel').get('name','')
            salarys=res.get('salary','')
            release_time=res.get('updateDate','')

            for key in self.key_words[zhuanye]:
                if key in title and self.pop_key[0] not in title and self.pop_key[1] not in title and self.pop_key[2] \
                        not in title and self.pop_key[3] not in title and '元/天' not in salarys:
                    # 岗位类型
                    job_type=get_type(title)
                    yield Request(url=url,meta={'zhuanye':zhuanye,'job_type':job_type,
                                                'title':title,'salarys':salarys,
                                                'company_name':company_name,'company_size':company_size,
                                                'company_type':company_type,'experience':experience,
                                                'education':education,'addr':addr,'release_time':release_time},
                                  callback=self.parse_detail)
                else:
                    continue

    def parse_detail(self,response):
        item_loader = ZhiLianItemLoader(item=ZhiLianItem(), response=response)
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
        item_loader.add_value('company_name',response.meta.get('company_name'))
        item_loader.add_value('company_type',response.meta.get('company_type'))
        item_loader.add_value('company_size',response.meta.get('company_size'))
        item_loader.add_value('experience',response.meta.get('experience'))
        item_loader.add_value('education',response.meta.get('education'))
        item_loader.add_value('phone','')
        item_loader.add_value('contact','')
        item_loader.add_xpath('company_addr','/html/body/div[6]/div[1]/div[1]/div/div[1]/h2/text()')
        item_loader.add_xpath('company_industry','/html/body/div[6]/div[2]/div[1]/ul/li[3]/strong/a/text()')
        item_loader.add_xpath('job_nums','/html/body/div[6]/div[1]/ul/li[last()-1]/strong/text()')
        job_desc=response.xpath("//div[@class='tab-cont-box']/div[1]/div/span/text() | //div[@class='tab-cont-box']/div[1]/p/text() | //div[@class='tab-cont-box']/div[1]/p/span/text() | //div[@class='tab-cont-box']/div[1]/text() | //div[@class='tab-cont-box']/div[1]/div/text() | //div[@class='tab-cont-box']/div[1]/pre/text()").extract()
        item_loader.add_value('job_desc',job_desc)

        yield item_loader.load_item()

    def genCrawlUrl(self):
        # 生成start_url
        for key in self.key_words.keys():
            for words in self.key_words.get(key):
                start_url = [self.base_start_url%(code,words,page,code,words) for code in self.code for page in range(1, self.page_num) ]
                yield start_url,key