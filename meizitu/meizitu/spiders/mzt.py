# -*- coding: utf-8 -*-
import re

import scrapy
import json
from meizitu.items import MeizituItem


class MztSpider(scrapy.Spider):
    name = 'mzt'
    allowed_domains = ['baidu.com']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

    # 指定url的情况下我们重写start_requests方法
    def start_requests(self):
        for i in range(21,40):
            start_urls='https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord+=&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&word=%E9%BB%91%E9%B9%B3&z=&ic=&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&step_word=%E9%BB%91%E9%B9%B3&pn={}&rn=30&gsm=3c'.format(30*i)
        # start_urls = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord+=&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&word=%E9%BB%91%E9%B9%B3&z=&ic=&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&step_word=%E9%BB%91%E9%B9%B3&pn=120&rn=30&gsm=3c'
            yield scrapy.Request(start_urls, headers=self.headers)

    def parse(self, response):
        # 从Json文件内容中提取所有img的内容
        item = MeizituItem()  # items中的类
        imgs = json.loads(response.body)['data']
        for eachImage in imgs:
            try:
                item['image_urls'] = [eachImage['middleURL']]
                yield item
            except Exception as e:
                print(e)