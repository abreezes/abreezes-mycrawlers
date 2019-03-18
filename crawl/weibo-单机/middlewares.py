# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

import demjson
import random

from scrapy import signals
from fake_useragent import UserAgent

import base64
import requests



class WeiboSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WeiboDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomProxyMiddleware(object):
    #动态设置ip代理
    proxies=''
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=https%3A%2F%2Fweibo.com%2F&domain=.weibo.com&ua=php-sso_sdk_client-0.6.28&_rand=1544352340.1551',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'If-Modified-Since': 'Sun, 09 Dec 2018 10:45:41 GMT',
    }

    def __init__(self,crawler):
        super(RandomProxyMiddleware,self).__init__()
        self.proxy_user=crawler.settings.get('PROXY_USER')
        self.proxy_passwd=crawler.settings.get('PROXY_PASSWD')
        self.proxy_server = crawler.settings.get('PROXY_SERVER')
        self.proxy_auth = "Basic " + base64.urlsafe_b64encode(bytes((self.proxy_user + ":" + self.proxy_passwd), "ascii")).decode("utf8")


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)


    # def is_success(self):
    #     """测试是否可用"""
    #     # time.sleep(3)
    #     self.proxies = self.get_proxy().strip()
    #     proxies = {
    #         "http": "http://{}".format(self.proxies),
    #         "https": "https://{}".format(self.proxies),
    #     }
    #     response=requests.get(url='https://weibo.com/u/6675785345',headers=self.headers,proxies=proxies,timeout=5)
    #     if response.status_code==200:
    #         return True
    #     else:
    #         return False

    # def get_proxy(self):
    #     """获取代理"""
    #     # return requests.get(self.url).json()
    #     return requests.get(self.url).text


    def process_request(self, request, spider):
        request.meta["proxy"] = self.proxy_server

        request.headers["Proxy-Authorization"] = self.proxy_auth

        # if self.is_success():
        #     if request.url.startswith('https://'):
        #         request.meta["Proxy"] = 'https://{}'.format(self.proxies)
        #     else:
        #         request.meta["Proxy"] = 'http://{}'.format(self.proxies)
        # else:
        #     self.process_request(request,spider)

class RandomUserAgentMiddlware(object):
    #随机更换user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
        request.headers.setdefault('User-Agent', get_ua())

class CookieMiddleware(object):
    # key_list=["winner_cookies:weibo", "user_cookies:weibo"]


    def process_request(self,request,spider):
        cookies = demjson.decode(random.choice(spider.db.hvals("cookies:weibo")))
        request.cookies = cookies

        #-----验证码的---------

        # if 'm.weibo.cn' in request.url:
        #     # home/userInfo的cookie
        #     cookies=demjson.decode(random.choice(spider.db.hvals("user_cookies:weibo")))
        #
        # elif 'event.weibo.com' in request.url:
        #     # 抽奖微博的cookies
        #     cookies=demjson.decode(random.choice(spider.db.hvals("winner_cookies:weibo")))
        #
        # else:
        #     print(request.url)
        #     cookies=demjson.decode(random.choice(spider.db.hvals(random.choice(self.key_list))))

        # request.cookies = cookies









