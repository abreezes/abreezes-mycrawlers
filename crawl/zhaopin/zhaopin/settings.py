# -*- coding: utf-8 -*-

# Scrapy settings for zhaopin project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os


BOT_NAME = 'zhaopin'

SPIDER_MODULES = ['zhaopin.spiders']
NEWSPIDER_MODULE = 'zhaopin.spiders'


import sys
BaseDir=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,BaseDir)

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhaopin (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

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
#    'zhaopin.middlewares.ZhaopinSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'zhaopin.middlewares.ZhaopinDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'zhaopin.pipelines.ZhaopinPipeline': 300,
    # 异步mysql
    'zhaopin.pipelines.MysqlTwisterPipeline': 2,
}

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

# 配置下载图片的连接,从哪个建中获取的
IMAGES_URLS_FIELD='front_image_url'
# 配置绝对路径,如果是保存在其他服务器上需要另外设置
project_dir=os.path.abspath(os.path.dirname(__file__))
IMAGES_STORE=os.path.join(project_dir,'images')

MYSQL_HOST=''
MYSQL_DBNAME=''
MYSQL_USER='root'
MYSQL_PASSWORD=''
Table = ''

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"

# 搜索词
KeyWords={'楼宇智能化工程':['楼宇',],'数控技术与应用':['数控'],
          '汽车运用与维修':['汽车'],'制冷和空调设备运行与维修':['制冷','空调','暖通'],
          '模具制造技术':['模具','机械cad'],'工业机器人应用与维护':['机器人'],
          '自动化':['自动化'],'机电一体化技术应用':['机电'],
          '物联网应用技术专业':['物联网']}

# 采集最大页数
PageMax=30

# 厦门人才网start_url
XMRC_START_URL='https://www.xmrc.com.cn/net/info/Resultg.aspx?a=a&g=g&recordtype=1&searchtype=3&keyword={}&releasetime=15&worklengthflag=0&sortby=updatetime&ascdesc=Desc&PageIndex={}'

# 智联招聘start_url
ZL_START_URL='https://fe-api.zhaopin.com/c/i/sou?pageSize=60&cityId=%s&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=%s&kt=3&lastUrlQuery={"p":%s,"pageSize":"60","jl":"%s","kw":"%s","kt":"3"}'

# 无忧招聘start_url
WY_START_URL='https://search.51job.com/list/{},000000,0000,00,9,99,{},2,{}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
# 无忧地区代码
WY_ADDR_CODE = ['110200', '110400', '110300','110600']

# 智联地区
ZL_ADDR_CODE=['682', '685', '681','694']

SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_SELECT_FORMAT="%Y-%m"
SQL_DATE_FORMAT = "%Y-%m-%d"

# 标识
IDENT=1

POP_KEY=['包吃住','汽车大奖','汽车奖','汽车年终大奖']

# 设置Log级别:
LOG_LEVEL = 'INFO'

# 禁止重试:
RETRY_ENABLED = False



