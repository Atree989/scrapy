# -*- coding: utf-8 -*-
import scrapy


class BdSpider(scrapy.Spider):
    name = 'bd'
    allowed_domains = ['baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
