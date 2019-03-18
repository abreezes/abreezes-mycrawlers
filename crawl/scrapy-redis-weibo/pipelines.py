# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 导入ImagesPipeline继承该类重写方法实现自定义路径
import pymongo
from scrapy.pipelines.images import ImagesPipeline
# 使用该包可以避免很多编码问题
import codecs
import json
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi
from scrapy.exporters import JsonItemExporter
from weibo.items import WeiboItem,WeiboUserItem


class WeiboPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    """自定义json文件的导出"""
    def __init__(self):
        self.file=codecs.open('art.json','w',encoding='utf-8')

    def process_item(self, item, spider):
        """拦截item写入到json中"""
        lines=json.dumps(dict(item),ensure_ascii=False) +'\n'
        self.file.write(lines)
        return item
    def spider_close(self,spider):
        """关闭写入操作"""
        self.file.close()

class JsonItemExporterPopeline(object):
    """调用scrapy提供的json export导出json文件"""
    def __init__(self):
        self.file=open('artexp.json','wb')
        # 关键地方,实例化对象,传入文件对象
        self.exporter=JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        # 调用关闭方法
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        """拦截item写入到json中"""
        self.exporter.export_item(item)
        return item

class MysqlPipeline(object):
    """自定义数据插入到数据库中,采用同步的机制插入数据库"""
    def __init__(self):
        self.con=pymysql.connect(host='127.0.0.1',username='root',password='root',db='jobble')
        self.cursor=self.con.cursor()

    def process_item(self, item, spider):
        insert_sql="""insert into jobble(title,url,create_date,fav_nums) value (%s,%s,%s,%s)"""
        # execute 插入操作是同步,当数据量大的时候,插入数据速度跟不上解析速度就会出现插入堵塞
        self.cursor.execute(insert_sql,(item['title'],item['url'],item['create_date'],item['fav_nums']))
        self.con.commit()

class MysqlTwisterPipeline(object):
    """异步连接池插入数据"""
    def __init__(self,dbpool):
        self.dbpool=dbpool

    # 使用静态方法--> from_settings 获取settings配置
    @classmethod
    def from_settings(cls,settings):
        # 字典中的参数要与连接的参数一致
        dbparms=dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        db_pool=adbapi.ConnectionPool("pymysql",**dbparms)
        # 也可以采用方式
        #db_pool=adbapi.ConnectionPool("pymysql",host=settings['MYSQL_HOST'],db=settings['MYSQL_DBNAME'],...)

        return cls(db_pool)
    def process_item(self, item, spider):
        """使用twisted将mysql插入变成异步执行"""
        # 有时候异步插入可能会出现错误,他会返回一个query对象
        query=self.dbpool.runInteraction(self.do_insert,item)
        #使用adderrorback调用异常处理
        query.addErrback(self.handle_error)

    def handle_error(self,failure):
        """处理异步插入的异常"""
        print(failure)


    # def do_insert(self,cursor,item):
    #     """执行具体插入"""
    #     # 如果要插入front_image_path需要取数组的第一个值,因为他是个数据
    #     insert_sql="""insert into job_ta (title,url,create_date,fav_nums) value (%s,%s,%s,%s)"""
    #     cursor.execute(insert_sql,(item['title'],item['url_object_id'],item['create_date'],item['fav_nums']))

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)




# 自定义管道保存图片路径到image_path中
class  ArticleImagePipeline(ImagesPipeline):
    # 重写方法保存图片路径
    def item_completed(self, results, item, info):
        # 判断item中是否有front_image_path这个字段,
        if 'front_image_path' in item:
            for ok,value in results:
                image_file_path=value['path']
            item['front_image_path']=image_file_path
            return item

class MongoPipeline(object):
    collection_prize='weibo_prize'
    collection_user='weibo_user'
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri=mongo_uri
        self.mongo_db=mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'))

    def open_spider(self,spider):
        self.client=pymongo.MongoClient(self.mongo_uri)
        self.db=self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        if isinstance(item,WeiboItem):
            self.db[self.collection_prize].insert_one(dict(item))
        elif isinstance(item,WeiboUserItem):
            self.db[self.collection_user].insert_one(dict(item))

        # return item



