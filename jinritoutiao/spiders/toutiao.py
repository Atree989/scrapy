# -*- coding: utf-8 -*-
import scrapy
import json

from jinritoutiao.items import JinritoutiaoItem


class TtSpider(scrapy.Spider):
    name = 'tt'
    allowed_domains = ['toutiao.com']
    start_urls = ['https://www.toutiao.com/']
    keyword='性感'
    page=0
    def start_requests(self):
        url = self.start_urls[
                  0] + 'search_content/?offset={offset}&format=json&keyword={keyword}&autoload=true&count=20&cur_tab=1&from=search_tab'
        for page in range(0,10):
            yield scrapy.Request(url=url.format(offset=page,keyword=self.keyword),callback=self.parse)

    def parse(self, response):
        #print(response.text)
        data=json.loads(response.text)
        items=data['bird_data']
        result=JinritoutiaoItem()
        count=0
        self.page+=1

        for item in items:
            image_list = []
            try:
                print('page=%s,count=%s'%(self.page,count))
                result['abstract']=item['abstract']
                result['datetime']=item['datetime']
                result['keywords']=item['keywords']
                result['article_url']=item['article_url']
                result['title']=item['title']
                result['media_name']=item['media_name']
                images=item['image_detail']
                for img in images:
                    image_list.append(img['url'])
                result['image_url']=image_list
                count+=1
                yield result
            except KeyError:
                print('关键词不存在')
