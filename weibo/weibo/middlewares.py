# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging

import requests


class CookiesMiddleware():
    def __init__(self,cookies_pool_url):
        self.logger=logging.getLogger(__name__)
        self.cookies_pool_url=cookies_pool_url
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            cookies_pool_url=crawler.setting.get('COOKIES_POOL_URL'))
    def get_random_cookies(self):
        try:
            response=requests.get(self.cookies_pool_url)
            if response.status_code==200:
                return json.loads(response.text)
            return None
        except ConnectionError:
            return None
    def process_requests(self,spider,requests):
        cookies=self.get_random_cookies()
        if cookies:
            requests.cookies=cookies
            self.logger.debug('Using Cookies'+json.dump(cookies))
        else:
            self.logger.debug('No Valid Cookies')