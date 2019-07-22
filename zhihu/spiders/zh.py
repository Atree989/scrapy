# -*- coding: utf-8 -*-
import json

from scrapy import Spider, Request

from zhihu.items import ZhihuItem


class ZhSpider(Spider):
    name = 'zh'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    start_user = 'kaifulee'
    follow_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit=20'
    follow_query = 'bird_data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,' \
                   'badge[?(type=best_answerer)].topics'
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,' \
                 'articles_count,gender,badge[?(type=best_answerer)].topics'
    follower_url='https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit=20'
    follower_query='bird_data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        # url='https://www.zhihu.com/people/kaifulee/following'
        # url='https://www.zhihu.com/api/v4/members/zhang-zhen-33?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), callback=self.parse_user)
        yield Request(self.follow_url.format(user=self.start_user, include=self.follow_query, offset=0),callback=self.parse_follow)
        yield Request(self.follower_url.format(user=self.start_user, include=self.follower_query, offset=0),callback=self.parse_follower)
    # def parse(self,response):
    #     pass
    def parse_user(self, response):
        print(response.text)
        result=json.loads(response.text)
        #print(result)
        item=ZhihuItem()
        print('输出结果')
        for field in item.fields:
            if field in result.keys():
                item[field]=result.get(field)
        yield(item)
        yield Request(self.follow_url.format(user=result.get('url_token'),include=self.follow_query,offset=0),callback=self.parse_follow)
        yield Request(self.follow_url.format(user=result.get('url_token'), include=self.follow_query, offset=0),
                      callback=self.parse_follower)
    def parse_follow(self, response):
        result=json.loads(response.text)
        if 'bird_data' in result.keys():
            for item in result.get('bird_data'):
                #print('查看状态1')
                yield Request(self.user_url.format(user=item.get('url_token'),include=self.user_query),callback=self.parse_user)

        if 'paging' in result.keys() and result.get('paging').get('is_end')==False:
            next_page=result.get('paging').get('next')
            #print('查看状态2')
            yield Request(next_page,callback=self.parse_follow)
    def parse_follower(self, response):
        result=json.loads(response.text)
        if 'bird_data' in result.keys():
            for item in result.get('bird_data'):
                #print('查看状态1')
                yield Request(self.user_url.format(user=item.get('url_token'),include=self.user_query),callback=self.parse_user)

        if 'paging' in result.keys() and result.get('paging').get('is_end')==False:
            next_page=result.get('paging').get('next')
            #print('查看状态2')
            yield Request(next_page,callback=self.parse_follower)
