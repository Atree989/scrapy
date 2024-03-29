# -*- coding: utf-8 -*-
from scrapy import Spider,FormRequest


class WbSpider(Spider):
    name = 'wb'
    allowed_domains = ['www.weibo.cn']
    start_urls = 'https://weibo.cn/search/mblog'
    max_page=100
    keyword='000001'
    def start_requests(self):
        url='{url}?hideSearchFrame=&keyword={keyword}'.format(url=self.start_urls,keyword=self.keyword)
        for page in range(self.max_page+1):
            data={
                'mp':str(self.max_page),
                'page':str(page)
            }
            yield FormRequest(url=url,callback=self.parse_index,formdata=data)
    def parse_index(self, response):
        print(response.text)
