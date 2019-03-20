
from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#配置调试命令
execute(['scrapy','crawl','qcwy'])
#execute(['scrapy','crawl','xmrc','-s','JOBDIR=crawls/xmrc/xmrcspider-1'])
#execute(['scrapy','crawl','qcwy','-s','JOBDIR=crawls/qcwy/qcwyspider-1'])
#execute(['scrapy','crawl','zhilian','-s','JOBDIR=crawls/zhilian/zhilianspider-1'])