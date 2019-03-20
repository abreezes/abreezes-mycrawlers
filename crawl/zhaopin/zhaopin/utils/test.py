
import requests
from lxml import etree
import time

re=requests.get('https://fe-api.zhaopin.com/c/i/sou?pageSize=60&cityId=%E6%B3%89%E5%B7%9E&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=%E7%A9%BA%E8%B0%83&kt=3&lastUrlQuery=%7B%22pageSize%22:%2260%22,%22jl%22:%22%E6%B3%89%E5%B7%9E%22,%22kw%22:%22%E7%A9%BA%E8%B0%83%22,%22kt%22:%223%22%7D').json()
print(re)
#info=etree.HTML(re)
#print(info)
#print(info.xpath("string(//*[@id='ctl00$Body$JobRepeaterPro_main_div']/table[2]/tr[6]/td[2]/a)").strip())

#list1=info.xpath("//*[@id='ctl00$Body$JobRepeaterPro_main_div']/table[2]/tr/td[2]/a")
#titles_list = [i for i in list1 if '实习' or '兼职' not in i.xpath('string(.)').strip()]

# print(''.join(info.xpath("//div[@class='bmsg inbox']/p[@class='fp']/text()")).strip())
# titles_list=info.xpath('//*[@id="resultList"]/div[@class="el"]/span[3]')
# for i in titles_list:
#     i.xpath('./text()')


print(time.strftime('%Y-%m'))

# value='3.5-7千/月'
# value2='5-7千/月'
# import re
# s=re.match(r'(\d+|\d.+)?-(\d+)?千/月',value)
# print(str(float(s.group(1))*1000)+'-'+str(float(s.group(2))*1000)+'元/月')
#
# val='福州-闽侯县  |  无工作经验  |  招40人  |  08-27发布'
# vs=''.join(val).split('  |  ')
# print(vs)
#
#
# x = """
#
# 新能源轻量化公司（尚干）"""
# print(lambda x: ''.join(x).strip())
# lambda x:x.strip()

import re
# value='6000-12000元/月'
# max_re=re.match('(\d+)-(\d+)?',value)
# if max_re:
#     #max_salary=(max_re.group(1))
#     print(max_re.group(1),max_re.group(2))
# #
# min_re=re.match('.+?-(\d+)?',value)
# min_salary = (min_re.group(1))
# print(min_salary)
#
# max_re=re.match('(\d+)?-',value)
# print(max_re.group(1))
#
# value='\r\n                                参考月薪：\xa06000-8000元/月\r\n                            '
# print(value.strip())
# mach_re = re.match(r'(\d+)-(\d+)', value)
# if mach_re:
#     salary = mach_re.group()
#     print(salary)
# else:
#     salary = '不限'
# value=' 2018-08-28 2018-09-27 09:49 '
# pattern = re.compile(r'.*?(\d{4}-\d{1,2}-\d{1,2})')
# print(re.match(pattern=pattern, string=value).group())

# def get_experience(value):
#     """工作经验"""
#     if value:
#         if '二年工作经验以上' or '2年经验' in value:
#             print('12222')
#             exp = '二年工作经验'
#         elif '一年工作经验以上' or '1年经验' in value:
#             print('1111')
#             exp = '一年工作经验'
#
#         elif '不限' or '无工作经验' in value:
#             exp = '不限'
#         else:
#             exp = '三年工作经验以上'
#     else:
#         exp = '不限'
#     return exp


val='福州-闽侯县  |  1工作经验  |  招40人  |  08-27发布'
vs=''.join(val).split('  |  ')
print(vs)

def get_experience(value):
    """工作经验"""
    if value:
        if  ('2年经验'or'二年工作经验以上') == value:
            print('12222')
            exp = '二年工作经验'
        elif  ('1年经验'or'一年工作经验') == value:
            print('1111')
            exp = '一年工作经验'

        elif ('无工作经验'or'不限') == value:
            exp = '2不限'
        else:
            exp = '三年工作经验以上'
    else:
        exp = '不限'
    return exp


def get_wy_experience(value):
    print(value)
    res=','.join(value)
    print(res)
    r=re.match(r'.*?,(.+经验)?',res)
    print(r.group(1))

def get_education(value):
    """学历"""
    if value:
        if ('高中'or'高中以上'or'中专'or'中专以上'or'初中以上'or'初中及以下'or'小学以上'or'中技') in value:
            edu = '中专及以下'
        elif ('大专以上'or'大专') in value:
            edu = '大专及以上'
        elif '不限' in value:
            edu = '不限'
        else:
            edu = '本科及以上'
    else:
        edu = '不限'
    print(edu)
    return edu


def get_wy_education(value):
    for v in value:
        if ('高中'or'小学以上'or'中专'or'初中及以下'or'不限'or'大专'or'中技'or'本科') in v:
            print(type(v))
            print('1111')
            get_education(v)
    else:
        print('99999')






get_wy_experience(vs)
print(get_wy_education(vs))

POP_KEY=['包吃住','汽车大奖','汽车奖']
print(POP_KEY[1])



