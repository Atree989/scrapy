# -*- coding: utf-8 -*-
import scrapy
import json
from Fire.items import FireItem
from scrapy.http import Request


class FireSpider(scrapy.Spider):
    name = 'fire'
    # 设置headers伪装成浏览器
    allowed_domains = ['baidu.com']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    # start_urls = ['http://image.baidu.com']

    # 指定url的情况下我们重写start_requests方法
    def start_requests(self):
        classes = []
        with open('cat', 'r',encoding='utf-8') as f:
            for line in f.readlines():
                clas = line.split(',')[0]
                classes.append(clas.strip())
        for i in range(len(classes)):
            for j in range(1,10):
                start_urls='https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={w1}' \
                           '&cl=2&lm=&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word={w2}&s=&se=&tab=&width=&height=' \
                           '&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={pn}&rn=30&gsm=1e'.format(w1=classes[i],w2=classes[i],pn=30*j)
        # start_urls = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord+=&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&word=%E9%BB%91%E9%B9%B3&z=&ic=&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&step_word=%E9%BB%91%E9%B9%B3&pn=120&rn=30&gsm=3c'
                yield scrapy.Request(start_urls, headers=self.headers,dont_filter=True)

    # json 解析
    def parse(self, response):
        # 从Json文件内容中提取所有img的内容
        item = FireItem()  # items中的类
        res_json = json.loads(response.body)
        imgs = res_json['data']
        group_name = res_json['queryExt']
        item['image_group_name'] = group_name
        for eachImage in imgs:
            try:
                item['image_urls'] = [eachImage['middleURL']]
                yield item
            except Exception as e:
                print(e)

    # # 文本解析
    # def start_requests(self):
    #     classes = []
    #     with open('cat', 'r',encoding='utf-8') as f:
    #         for line in f.readlines():
    #             clas = line.split(',')[1]
    #             classes.append(clas.strip())
    #     for i in range(len(classes)):
    #         start_url = 'https://image.baidu.com/search/index?tn=baiduimage&word={}'.format(classes[i])
    #         yield scrapy.Request(start_url, headers=self.headers, dont_filter=True)
    #
    # def parse(self,response):
    #     item = DogsItem()
    #     result = response.text
    #     ids = response.xpath('//*[@id="imgid"]').extract()
    #     # item['image_group_name'] = group_name
    #     for id in ids:
    #         try:
    #             item['image_urls'] = [id['middleURL']]
    #             yield item
    #         except Exception as e:
    #             print(e)
