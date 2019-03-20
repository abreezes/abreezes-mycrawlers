# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst,Join
import re,time
from settings import SQL_DATE_FORMAT,Table


class ZhaopinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def date_convert(value):
    """日期转换"""
    # 也可以写表达式
    try:
        create_date = datetime.datetime.strptime(value, '%Y/%m/%d').date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date

def get_num(value):
    match_re = re.match(".*?(\d+).*",value)
    if match_re:
        num = match_re.group(1)
    else:
        num = 0
    return num

'-----------厦门人才网处理与公用方法---------------'

def remove_title(value):
    """去除标题"""
    if value:
        return value.strip()[6:].strip()
    else:
        return None

def get_salary(value):
    """薪资"""
    salary=0
    if value.strip():
        mach_re = re.match(r'(\d+)-(\d+)元/月', value)
        if mach_re:
            salary=mach_re.group()
        elif value == '面议':
            salary=salary
        else:
            salary=salary
    else:
        salary=salary
    return salary

def get_experience(value):
    """工作经验"""
    if value:
        if value == '一年工作经验以上' or value == '1年经验' or value == '1-3年':
            exp = '一年工作经验'
        elif value == '二年工作经验以上' or value == '2年经验' or value == '1-3年':
            exp = '二年工作经验'
        elif value == '不限' or value == '无工作经验':
            exp = '不限'
        else:
            exp = '三年工作经验以上'
    else:
        exp = '不限'
    return exp

def get_education(value):
    """学历"""
    if value:
        if value == '高中' or value == '高中以上' or value == '中专' or value == '中专以上' or value == '初中以上' or value == '初中及以下' or value == '小学以上' or value == '中技':
            edu = '中专及以下'
        elif value == '大专以上' or value == '大专':
            edu = '大专及以上'
        elif value == '不限':
            edu = '不限'
        else:
            edu = '本科及以上'
    else:
        edu = '不限'
    return edu

def get_max_salary(value):
    """最高薪资"""
    max_salary=0
    if value.strip():
        max_re = re.match('(\d+)?-', value)
        if max_re:
            max_salary=(max_re.group(1))
        elif value == '面议':
            max_salary = max_salary
        else:
            max_salary = max_salary
    else:
        max_salary= max_salary
    return max_salary

def get_min_salary(value):
    """最低薪资"""
    min_salary=0
    if value.strip():
        min_re = re.match('.+?-(\d+)?', value)
        if min_re:
            min_salary =min_re.group(1)
        elif value == '面议':
            min_salary=min_salary
        else:
            min_salary=min_salary
    else:
        min_salary=min_salary
    return min_salary

def get_phone(value):
    """联系电话"""
    if value:
        if value == '(合则约见、谢绝来电)':
            phone='*******'
        else:
            return value
    else:
        phone='*******'
    return phone

def get_jobdesc(value):
    """岗位职责"""
    job_desc=''
    for i in value:
        job_desc+=i.strip()
    return job_desc

def get_release_time(value):
    """发布时间"""
    mach_re=re.match(r'.*?(\d{4}-\d{1,2}-\d{1,2})',value)
    if mach_re:
        release_time=mach_re.group()
    else:
        release_time=time.strftime('%Y-%m-%d')
    return release_time

def get_job_num(value):
    """招聘人数"""
    num = '若干'
    if value.strip():
        if value == '若干':
            num=num
        else:
            return value
    else:
        num = num
    return num

def get_company_size(value):
    if value:
        if value == '少于50人' or value == '20人以下' :
            size='少于50人'
        elif value == '50-150人' or value == '20-99人':
            size='50-150人'
        elif value == '150-500人' or value == '100-499人':
            size='150-500人'
        else:
            size='大于500人'
        return size
    else:
        return '少于50人'

def get_company_type(value):
    if value:
        if value == '外商独资' or value == '外商合资' or value == '外资(非欧美)' or value == '外资(欧美)':
            val = '外资'
        elif value == '合资' or value == '上市公司' or value == '股份制企业' or value == '民营':
            val = '民营公司'
        elif value == '国企' or value == '事业':
            val = '国企单位'
        else:
            val = '其它'
        return val
    else:
        return '其它'

'--------------厦门人才网item--------------------'

class XmrcItemLoader(ItemLoader):
    """自定义itemloader"""
    # 可以使用自定义让它只获取到itemloader列表中的第一个
    default_output_processor = TakeFirst()

class XmrcItem(scrapy.Item):
    company_name=scrapy.Field(
        input_processor=MapCompose(remove_title)
    )
    company_addr=scrapy.Field(
        input_processor=MapCompose(remove_title,lambda x:x[:-11])
    )
    salarys=scrapy.Field(
        input_processor=MapCompose(remove_title,get_salary)
    )
    max_salary=scrapy.Field(
        input_processor=MapCompose(remove_title,get_salary,get_max_salary)
    )
    min_salary=scrapy.Field(
        input_processor=MapCompose(remove_title,get_salary,get_min_salary)
    )
    experience=scrapy.Field(
        input_processor=MapCompose(remove_title,get_experience)
    )
    education=scrapy.Field(
        input_processor=MapCompose(remove_title,get_education)
    )
    job_desc=scrapy.Field(
        input_processor=MapCompose(get_jobdesc),
        output_processor=Join('')
    )
    phone=scrapy.Field(
        input_processor=MapCompose(remove_title,get_phone)

    )
    contact=scrapy.Field(
        input_processor=MapCompose(remove_title)
    )
    release_time=scrapy.Field(
        input_processor=MapCompose(remove_title,get_release_time)
    )
    job_nums = scrapy.Field(
        input_processor=MapCompose(get_job_num)
    )
    job_type=scrapy.Field()
    ident=scrapy.Field()
    object_id=scrapy.Field()
    company_type = scrapy.Field()
    company_size = scrapy.Field()
    company_industry = scrapy.Field()
    select_time=scrapy.Field()
    crawl_time=scrapy.Field()
    crawl_name=scrapy.Field()
    zhuanye=scrapy.Field()
    addr=scrapy.Field()
    title=scrapy.Field()
    link=scrapy.Field()

    def get_insert_sql(self):
        return insert(self)

'--------------前程无忧清洗方法----------------'

def get_wy_salary(value):
    """无忧薪资格式化"""
    if value:
        if '千/月' in value:
            mach_re=re.match(r'(\d+|\d.+)?-(\d+|\d.+)?千/月', value)
            if mach_re:
                one=float(mach_re.group(1)) * 1000
                two=float(mach_re.group(2)) * 1000
                salary = str(('%.0f' % one)) + '-' + str(('%.0f' % two)) + '元/月'
                return salary

        elif '万/月' in value:
            mach_re = re.match(r'(\d+|\d.+)?-(\d+|\d.+)?万/月', value)
            if mach_re:
                one = float(mach_re.group(1)) * 10000
                two = float(mach_re.group(2)) * 10000
                salary = str(('%.0f' % one)) + '-' + str(('%.0f' % two)) + '元/月'
                return salary

        elif '万/年' in value:
            mach_re = re.match(r'(\d+|\d.+)?-(\d+|\d.+)?万/年', value)
            if mach_re:
                one = float(mach_re.group(1)) * 10000
                two = float(mach_re.group(2)) * 10000
                salary = str(('%.0f' %(one/12))) + '-' + str(('%.0f' %(two/12))) + '元/月'
                return salary

        else:
            return '面议'
    else:
        return '面议'

def get_wy_spilt(value):
    """切隔"""
    val=','.join(value.split('\xa0\xa0|\xa0\xa0'))
    return val

def get_wy_experience(value):
    #val=''.join(value)
    res=re.match(r'.*?,(.+经验)?.*',value)
    if res:
        red=res.group(1)
        return red
    else:
        return '不限'

def get_wy_education(value):
    #val = ''.join(value)
    res = re.match(r'.*?,(高中|小学以上|中专|初中及以下|大专|中技|本科|本科及以上).*', value)
    if res:
        red=res.group(1)
        return red
    else:
        return '不限'

def get_wy_job_nums(value):
    #val=''.join(value)
    res=re.match(r'.*?,招(.+)?人.*',value)
    if res:
        red=res.group(1)
        return red
    else:
        return '若干'

'---------------前程无忧item--------------------------'

class WuYouItemLoader(ItemLoader):
    """自定义itemloader"""
    # 可以使用自定义让它只获取到itemloader列表中的第一个
    default_output_processor = TakeFirst()


class WuYouItem(scrapy.Item):
    company_name=scrapy.Field()
    company_addr=scrapy.Field(
        input_processor=MapCompose(lambda x:''.join(x).strip())
    )
    salarys=scrapy.Field(
        input_processor=MapCompose(get_wy_salary)
    )
    max_salary=scrapy.Field(
        input_processor=MapCompose(get_wy_salary,get_max_salary)
    )
    min_salary=scrapy.Field(
        input_processor=MapCompose(get_wy_salary,get_min_salary)
    )
    experience=scrapy.Field(
        input_processor=MapCompose(get_wy_spilt,get_wy_experience,get_experience)
    )
    education=scrapy.Field(
        input_processor=MapCompose(get_wy_spilt,get_wy_education,get_education)
    )
    job_nums = scrapy.Field(
        input_processor=MapCompose(get_wy_spilt,get_wy_job_nums,get_job_num)
    )
    job_desc=scrapy.Field(
        input_processor=MapCompose(get_jobdesc),
        output_processor=Join('')
    )
    company_size = scrapy.Field(
        input_processor=MapCompose(get_company_size)
    )
    company_type = scrapy.Field(
        input_processor=MapCompose(get_company_type)
    )


    phone=scrapy.Field()
    contact=scrapy.Field()
    release_time=scrapy.Field()
    job_type=scrapy.Field()
    ident=scrapy.Field()
    object_id=scrapy.Field()
    company_industry = scrapy.Field()
    select_time=scrapy.Field()
    crawl_time=scrapy.Field()
    crawl_name=scrapy.Field()
    zhuanye=scrapy.Field()
    addr=scrapy.Field()
    title=scrapy.Field()
    link=scrapy.Field()

    def get_insert_sql(self):

        return insert(self)


'----------------智联招聘--------------------------'
def get_zl_salary(value):
    """无忧薪资格式化"""
    if value:
        mach_re=re.match(r'(\d+|\d.+)?K-(\d+|\d.+)?K', value)
        if mach_re:
            one=float(mach_re.group(1)) * 1000
            two=float(mach_re.group(2)) * 1000
            salary = str(('%.0f' % one)) + '-' + str(('%.0f' % two)) + '元/月'
            return salary
        else:
            return '面议'
    else:
        return '面议'


class ZhiLianItemLoader(ItemLoader):
    """自定义itemloader"""
    # 可以使用自定义让它只获取到itemloader列表中的第一个
    default_output_processor = TakeFirst()


class ZhiLianItem(scrapy.Item):

    salarys = scrapy.Field(
        input_processor=MapCompose(get_zl_salary)
    )
    max_salary = scrapy.Field(
        input_processor=MapCompose(get_zl_salary, get_max_salary)
    )
    min_salary = scrapy.Field(
        input_processor=MapCompose(get_zl_salary, get_min_salary)
    )
    experience = scrapy.Field(
        input_processor=MapCompose(get_experience)
    )
    education = scrapy.Field(
        input_processor=MapCompose(get_education)
    )
    job_nums = scrapy.Field(
        input_processor=MapCompose(lambda x:x.strip()[:-1])
    )
    company_size = scrapy.Field(
        input_processor=MapCompose(get_company_size)
    )
    company_type = scrapy.Field(
        input_processor=MapCompose(get_company_type)
    )
    release_time = scrapy.Field(
        input_processor=MapCompose(get_release_time)
    )
    job_desc = scrapy.Field(
        input_processor=MapCompose(get_jobdesc),
        output_processor=Join('')
    )

    company_name = scrapy.Field()
    company_addr = scrapy.Field(
        input_processor=MapCompose(lambda x:x.strip()),
    )
    phone = scrapy.Field()
    contact = scrapy.Field()
    job_type = scrapy.Field()
    ident = scrapy.Field()
    object_id = scrapy.Field()
    company_industry = scrapy.Field()
    select_time = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_name = scrapy.Field()
    zhuanye = scrapy.Field()
    addr = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()


    def get_insert_sql(self):

        return insert(self)

'-------生成sql语句------------------'
def insert(value):
    table = Table
    keys = ','.join(value.keys())
    values = ','.join(['%s', ] * len(value))

    insert_sql = """INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE title=VALUES(title),salarys=VALUES(salarys),max_salary=VALUES(max_salary),min_salary=VALUES(min_salary),job_nums=VALUES(job_nums),job_desc=VALUES(job_desc)""".format(
        table=table, keys=keys, values=values)

    params = tuple(value.values())
    return insert_sql, params





