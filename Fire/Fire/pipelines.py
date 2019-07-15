# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# import pymongo
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import re

i = 0
class FirePipeline(object):
    def process_item(self, item, spider):
        return item

class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print('item=',item)
        for img_url in item['image_urls']:
            yield scrapy.Request(url=img_url,headers={'Referer': item['image_urls'][0]}, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        global i
        item=request.meta['item']
        # index = item['image_name']
        # print('index', index)
        name = '%.3d'%i + '.jpg'
        i += 1
        folder=item['image_group_name']
        #image_guide=index+'.'+request.url.split('/')[-1].split('.')[-1]
        filename=u'/{0}/{1}'.format(folder,name)
        print('filename',filename)
        print('保存图像成功')

        return filename

class MongoPipeline(object):
    collection_name = 'scrapy_items'
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db['info'].insert(dict(item))
        print('存储到MONGODB成功')
        return item