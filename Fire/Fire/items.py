# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FireItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_title=scrapy.Field()
    image_urls=scrapy.Field()
    class_title=scrapy.Field()
    class_url=scrapy.Field()
    group_url=scrapy.Field()
    group_title=scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()

    image_group_name=scrapy.Field()
    image_group_url=scrapy.Field()
    image_name=scrapy.Field()
