# -*- coding: utf-8 -*-
import scrapy

from items import JobBoleArticleItem,ArticleItemLoader
from utils import common


class JobbleeSpider(scrapy.Spider):
    name = 'jobblee'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']
    #
    # def __init__(self):
    #     self.brower = webdriver.Chrome(executable_path=r"C:/Python36/chromedriver.exe")
    #     super(JobbleeSpider,self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    #
    # def spider_closed(self,spider):
    #     self.brower.quit()


    def parse(self, response):
        select_html=response.xpath('//div[@class="grid-8"]/div[@class="post floated-thumb"]/div[@class="post-meta"]/p/a[1]/@href').extract()
        img_url=response.xpath('//div[@class="grid-8"]/div[@class="post floated-thumb"]/div[@class="post-thumb"]/a[1]/img/@src').extract()
        for post_url,image_url in zip(select_html,img_url):
            # 此处使用meta穿参数
            yield scrapy.Request(url=post_url,callback=self.parse_detail,meta={'front_image_url':image_url,"JsPage":True},dont_filter=True)
        page_url=response.xpath('//div/a[@class="next page-numbers"]/@href').extract_first('')
        if page_url:
            yield scrapy.Request(url=page_url,callback=self.parse)

    def parse_detail(self,response):

        #article_item=JobBoleArticleItem()

        # article_item['title']=response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        # #
        # # # 提取meta中的值,使用get方法遇到空的键值才不会报错,默认值为空,此处使用的是元祖非[]
        # # # image的url要改为数组,不然在使用自动下载器会报错,即setting中的IMAGES_URLS_FILELD
        # article_item['front_image_url']=[response.meta.get('front_image_url','')]
        # date_time=re.match('.*?(\d{4}/\d+/\d+).*',response.xpath('//div/p[@class="entry-meta-hide-on-mobile"]/text()[1]').extract()[0])
        # try:
        #     article_item['create_date']=datetime.datetime.strptime(date_time,'%Y/%m/%d').date()
        # except Exception as e:
        #     article_item['create_date']=datetime.datetime.now().date()
        # article_item['tag']=','.join(response.xpath('//div/p[@class="entry-meta-hide-on-mobile"]/a/text()').extract())
        # article_item['content']=''.join(response.xpath('//div[@class="entry"]/p/text()').extract())
        # article_item['praise_nums']=response.xpath('//div[@class="post-adds"]/span/h10/text()').extract()[0]
        # fav_num=response.xpath('//div[@class="post-adds"]/span[2]/text()').extract()[0]
        # match_re=re.match(".*?(\d+).*",fav_num)
        # if match_re:
        #     article_item['fav_nums']=match_re.group(1)
        # else:
        #     article_item['fav_nums']=0
        # comment_num=response.xpath('//div[@class="post-adds"]/a/span/text()').extract()[0]
        # match_re = re.match(".*?(\d+).*", comment_num)
        # if match_re:
        #     article_item['comment_nums'] = match_re.group(1)
        # else:
        #     article_item['comment_nums']=0
        # article_item['url_object_id'] =common.get_md5(response.url)

        # 使用ItemLoader加载item
        #item_loader=ItemLoader(item=JobBoleArticleItem(),response=response)
        # 使用自定义ArticleItemLoader
        item_loader=ArticleItemLoader(item=JobBoleArticleItem(),response=response)
        item_loader.add_xpath('title','//div[@class="entry-header"]/h1/text()')
        item_loader.add_xpath('tag','//div/p[@class="entry-meta-hide-on-mobile"]/a/text()')
        item_loader.add_value('front_image_url',[response.meta.get('front_image_url','')])
        item_loader.add_value('url',response.url)
        item_loader.add_xpath('content','//div[@class="entry"]/p/text()')
        item_loader.add_xpath('praise_nums','//div[@class="post-adds"]/span/h10/text()')
        item_loader.add_xpath('comment_nums','//div[@class="post-adds"]/a/span/text()')
        item_loader.add_xpath('fav_nums','//div[@class="post-adds"]/span[2]/text()')
        item_loader.add_xpath('create_date','//div/p[@class="entry-meta-hide-on-mobile"]/text()[1]')
        item_loader.add_value('url_object_id',common.get_md5(response.url))


        article_item=item_loader.load_item()


        yield article_item
        pass