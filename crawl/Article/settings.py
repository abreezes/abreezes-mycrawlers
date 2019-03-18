# -*- coding: utf-8 -*-
import os
# Scrapy settings for Article project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Article'

SPIDER_MODULES = ['Article.spiders']
NEWSPIDER_MODULE = 'Article.spiders'

import sys
BaseDir=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,BaseDir)

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Article (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Article.middlewares.ArticleSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #'Article.middlewares.JSPageMiddleware': 1,
    'Article.middlewares.RandomUserAgentMiddlware': 2,
    'Article.middlewares.RandomProxyMiddleware': 1,
    #'Article.middlewares.ArticleSpiderMiddleware':3,

    #'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,

}


# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   #'Article.pipelines.ArticlePipeline': 300,
   # 'Article.pipelines.JsonWithEncodingPipeline':2,
    #'Article.pipelines.JsonItemExporterPopeline':2,
   #配置图片自动下载器,数值越小,优先权越高
   #'scrapy.pipelines.images.ImagesPipeline':1,
    # 同步mysql
    #'Article.pipelines.MysqlPipeline': 2,
    # 异步mysql
    'Article.pipelines.MysqlTwisterPipeline': 2,


   # 配置自定义的保存image管道
    #'Article.pipelines.ArticleImagePipeline':1,

}
# 配置下载图片的连接,从哪个建中获取的
IMAGES_URLS_FIELD='front_image_url'
# 配置绝对路径,如果是保存在其他服务器上需要另外设置
project_dir=os.path.abspath(os.path.dirname(__file__))
IMAGES_STORE=os.path.join(project_dir,'images')

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_HOST='127.0.0.1'
MYSQL_DBNAME='tianyancha'
MYSQL_USER='root'
MYSQL_PASSWORD='root'

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"

RANDOM_UA_TYPE = "random"

TIANYANNUM={
    '0':'2',
    '1':'6',
    '2':'3',
    '3':'1',
    '4':'0',
    '5':'9',
    '6':'5',
    '7':'7',
    '8':'4',
    '9':'8',
    '-':'-'
}
SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"