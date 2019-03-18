# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst,Join
import scrapy
import re
from settings import TIANYANNUM
from settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT


class ArticleItem(scrapy.Item):
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

class ArticleItemLoader(ItemLoader):
    """自定义itemloader"""
    # 可以使用自定义让它只获取到itemloader列表中的第一个
    default_output_processor = TakeFirst()

def get_num(value):
    match_re = re.match(".*?(\d+).*",value)
    if match_re:
        num = match_re.group(1)
    else:
        num = 0
    return num

def return_value(value):
    return value

def convert_get_date(value):
    date=''
    for k in value:
        date+=TIANYANNUM[k]
    return date



# 限定为jobble的域名
class JobBoleArticleItem(scrapy.Item):
    # MapCompose可以传匿名函数,也可以传两个函数
    title=scrapy.Field(
        input_processor=MapCompose(lambda x:x+'-jobbole',),
        # 使用TakeFirst取出列表中的第一个
        # 使用可自定义itemloader就可以不用当下的
        #out_processor=TakeFirst()
    )
    create_date=scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    front_image_url=scrapy.Field(
        # 图片下载器用的是数组不是字符串,所以不适合使用自定义的itemloader,解决方法定义处理函数什么都不做,覆盖掉TakeFirst()处理
        # url不是数组会抛出异常
        output_processor=MapCompose(return_value)
    )
    front_image_path=scrapy.Field()
    fav_nums=scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    comment_nums=scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    praise_nums=scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    tag=scrapy.Field(
        # 使用join把列表内容转成字符串,不需要使用自定义itemloader获取列表中的第一个就用该方式,在此处重新out_processor
         output_processor=Join(',')
    )
    content=scrapy.Field()

class TianYanChaItemLoader(ItemLoader):
    """自定义itemloader"""
    # 可以使用自定义让它只获取到itemloader列表中的第一个
    default_output_processor = TakeFirst()

class TianYanChaItem(scrapy.Item):
    compname=scrapy.Field()
    phone=scrapy.Field()
    email=scrapy.Field()
    url=scrapy.Field()
    object_id=scrapy.Field()
    fddb=scrapy.Field()
    zczb=scrapy.Field()
    zctime=scrapy.Field(
        input_processor=MapCompose(convert_get_date)
    )
    gszt=scrapy.Field()
    gsid=scrapy.Field()
    orgid=scrapy.Field()
    gstype=scrapy.Field()
    xyid=scrapy.Field()
    nsrid=scrapy.Field()
    hy=scrapy.Field()
    yyqx=scrapy.Field()
    hzrq=scrapy.Field(
        input_processor=MapCompose(convert_get_date)
    )
    size=scrapy.Field()
    sjzb=scrapy.Field()
    djjg=scrapy.Field()
    addr=scrapy.Field()
    jyfw=scrapy.Field()
    zyry=scrapy.Field(
        output_processor=Join(',')
    )
    gdxx=scrapy.Field(
        output_processor=Join(',')
    )

    def get_insert_sql(self):
        #插入sql语句
        insert_sql = """
            insert into tianyancha(object_id,compname,email,phone,url,fddb,gsid,hy, zyry,
              gdxx, jyfw, crawl_time
              )
            VALUES (%s, %s, %s,%s,  %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE phone=VALUES(phone), zyry=VALUES(zyry), gdxx=VALUES(gdxx),
              jyfw=VALUES(jyfw)
        """

        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (self.get('object_id'),self.get('compname',''),self.get('email',''),self.get('phone',''),
                  self.get('url',''),self.get('fddb',''),self.get('gsid',''),
                  self.get('hy',''),self.get('zyry',''),self.get('gdxx',''),self.get('jyfw',''), crawl_time)

        return insert_sql, params

class ItJuZiItemLoader(ItemLoader):
    """自定义itemloader"""
    # 可以使用自定义让它只获取到itemloader列表中的第一个
    default_output_processor = TakeFirst()

class ItJuZiItem(scrapy.Item):

    com_name=scrapy.Field()
    object_id=scrapy.Field()
    url=scrapy.Field()
    com_url=scrapy.Field()
    com_tag=scrapy.Field(
        output_processor=Join(',')
    )
    com_slgan=scrapy.Field()
    com_desc=scrapy.Field()
    com_date=scrapy.Field()
    com_size=scrapy.Field()
    com_operation=scrapy.Field()
    com_rongzi=scrapy.Field(
        output_processor=Join(',')
    )
    com_itemer=scrapy.Field(
        output_processor=Join(',')
    )

    def get_insert_sql(self):
        #插入sql语句
        insert_sql = """
            insert into itjuzi(com_name,object_id,url,com_url,com_tag,com_slgan,com_desc,com_date,
             com_size,com_operation,com_rongzi,com_itemer
              )
            VALUES (%s, %s,%s,  %s, %s, %s, %s, %s, %s, %s, %s %s,%s,%s)
            ON DUPLICATE KEY UPDATE com_rongzi=VALUES(com_rongzi), com_rongzi=VALUES(com_rongzi)
        """

        params = (self.get('com_name'),self.get('object_id',''),self.get('url',''),self.get('com_url',''),
                  self.get('com_tag',''),self.get('com_slgan',''),self.get('com_desc',''),
                  self.get('com_date',''),self.get('com_size',''),self.get('com_operation',''),self.get('com_rongzi',''), self.get('com_itemer',''))

        return insert_sql, params








