# -*- coding: utf-8 -*-
__author__ = 'admin'
__date__ = '2018/8/8 18:41'


import re

cookie="_ga=GA1.2.1143260020.1533727056; gr_user_id=52a91c70-e03a-4436-8048-52f8cc7a9c3e; MEIQIA_EXTRA_TRACK_ID=18VmBsrmsc9sV10KFqY9bnV0Z7m; session=b97ed6aa47c04df036cfb94bd996ef66f00372f6; acw_tc=AQAAAHwP/GyVXgkAbt/JI00K2uDyIudZ; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1533737865,1533911273,1534075668,1534684270; _gid=GA1.2.962223990.1534684270; _gat=1; gr_session_id_eee5a46c52000d401f969f4535bdaa78=ce74e7a2-84fd-43bf-8aec-e01848af566c; gr_session_id_eee5a46c52000d401f969f4535bdaa78_ce74e7a2-84fd-43bf-8aec-e01848af566c=true; identity=17895983515%40test.com; remember_code=MvPjSZ5JFG; unique_token=612433; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1534684276"
item={}
cook=cookie.split(';')
for c in cook:
    key,value=c.split('=')
    item[key.strip()]=value.strip()
print(item)

s="""Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Host: radar.itjuzi.com
Proxy-Connection: keep-alive
Referer: http://radar.itjuzi.com//company
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
X-Requested-With: XMLHttpRequest"""

s = s.strip().split('\n')
s = {x.split(':')[0].strip():x.split(':')[1].strip() for x in s}
print(s)





