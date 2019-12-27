# -*- coding: utf-8 -*-
import scrapy
import json
from fans.items import RepostItem
import random
import time
from pymongo import MongoClient
from pandas.io.json import json_normalize

class GetrepostSpider(scrapy.Spider):
    name = 'getrepost'

    # 微博转发展示页面　　https://m.weibo.cn/detail/4441150947886558#repost
    # 微博转发api地址　　https://m.weibo.cn/api/statuses/repostTimeline?id=4441150947886558&page=1
    start_url = 'https://m.weibo.cn/api/statuses/repostTimeline?id={}&page={}'
    repost_page = 1
    max = 100
    # 需提供文章ｉｄ
    id = 4448036119673757
    user_agent = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]

    def start_requests(self):
        yield scrapy.Request(url=self.start_url.format(self.id,self.repost_page), callback=self.parse_repost)#meta={'proxy': 'https://{}'.format(self.proxy)}


    def parse_repost(self, response):
        html = response.text
        html = json.loads(html)
        if (self.repost_page == 1):
            self.max = html['data']['max']
        self.repost_page += 1
        next_url = self.start_url.format(self.id, self.repost_page)
        try:
            for i in range(len(html['data']['data'])):
                item = RepostItem()
                item['star_weibo_id'] = self.id
                item['created_at'] = html['data']['data'][i]['created_at']  # 转发时间
                item['repost_id'] = html['data']['data'][i]['id']  # 转发微博的ｉｄ
                item['source'] = html['data']['data'][i]['source']  # 发博设备
                item['id'] = html['data']['data'][i]['user']['id']  # 转发用户的ｉｄ
                item['user_screen_name'] = html['data']['data'][i]['user']['screen_name']
                item['profile_url'] = html['data']['data'][i]['user']['profile_url']
                item['statuses_count'] = html['data']['data'][i]['user']['statuses_count']  # 发表微博的数量
                item['verified'] = html['data']['data'][i]['user']['verified']
                item['description'] = html['data']['data'][i]['user']['description']
                item['gender'] = html['data']['data'][i]['user']['gender']
                item['mbtype'] = html['data']['data'][i]['user']['mbtype']
                item['urank'] = html['data']['data'][i]['user']['urank']  # 等级
                item['mbrank'] = html['data']['data'][i]['user']['mbrank']
                item['followers_count'] = html['data']['data'][i]['user']['followers_count']  # 粉丝数
                item['follow_count'] = html['data']['data'][i]['user']['follow_count']  # 关注数
                item['cover_image_phone'] = html['data']['data'][i]['user']['cover_image_phone']  # 头像
                item['avatar_hd'] = html['data']['data'][i]['user']['avatar_hd']  # 背景图片
                try:
                    item['badge'] = len(html['data']['data'][i]['user']['badge'])
                except:
                    item['badge'] = 0
                item['reposts_count'] = html['data']['data'][i]['reposts_count']
                item['comments_count'] = html['data']['data'][i]['comments_count']
                item['attitudes_count'] = html['data']['data'][i]['attitudes_count']
                item['pending_approval_count'] = html['data']['data'][i]['pending_approval_count']
                item['isLongText'] = html['data']['data'][i]['isLongText']
                item['raw_text'] = html['data']['data'][i]['raw_text']
                yield item
        except:
            print("no data")
        if self.repost_page <= self.max:
            headers = {
                'USER_AGENT': random.choice(self.user_agent)
            }
            if self.repost_page % 50 == 29:
                # self.proxy = random.choice(self.proxy_list)
                time.sleep(100)
            yield scrapy.Request(url=next_url, callback=self.parse_repost, headers=headers,
                             meta={'weibo_id': self.id})#, 'proxy': 'https://{}'.format(self.proxy)
