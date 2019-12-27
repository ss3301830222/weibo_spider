# -*- coding: utf-8 -*-
import scrapy
import scrapy
import json
from fans.items import CommentItem
import random
import time
from pymongo import MongoClient
from pandas.io.json import json_normalize


class GetcommentSpider(scrapy.Spider):
    name = 'getcomment'

    # 微博评论展示页面:https://m.weibo.cn/detail/4441150947886558#comment
    # 微博转发api地址:https://m.weibo.cn/comments/hotflow?id=4441150947886558&mid=4441150947886558&max_id_type=0
    start_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type={}'
    comment_page = 1
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

    headers = {
        'USER_AGENT': random.choice(user_agent)
    }
    # conn = MongoClient('127.0.0.1', 27017)
    # db = conn.proxy
    # mongo_proxy = db.good_proxy
    # proxy_data = mongo_proxy.find()
    # proxies = json_normalize([ip for ip in proxy_data])
    # proxy_list = list(proxies['ip'])
    # proxy = random.choice(proxy_list)

    def start_requests(self):
        yield scrapy.Request(url=self.start_url.format(self.id,self.id,0), callback=self.parse_comment,headers=self.headers,
                             cookies=self.settings['COOKIES'])#,meta={'proxy': 'https://{}'.format(self.proxy)}

    def parse_comment(self, response):
        self.comment_page += 1
        weibo_id = self.id
        html = response.text
        html = json.loads(html)

        try:
            data = html['data']['data']
            for i in range(len(data)):
                item = CommentItem()
                item['star_weibo_id'] = weibo_id
                item['created_at'] = data[i]['created_at']
                item['comment_id'] = data[i]['id']
                item['floor_number'] = data[i]['floor_number']
                item['text'] = data[i]['text']
                item['total_number'] = data[i]['total_number']  # 评论的评论数量
                item['isLikedByMblogAuthor'] = data[i]['isLikedByMblogAuthor']  # 评论者是否被明星博主关注
                item['like_count'] = data[i]['like_count']  # 评论的点赞数量
                user = data[i]['user']  # 评论者的信息
                item['id'] = user['id']
                item['screen_name'] = user['screen_name']
                item['profile_image_url'] = user['profile_image_url']
                item['profile_url'] = user['profile_url']
                item['statuses_count'] = user['statuses_count']
                item['verified'] = user['verified']
                item['description'] = user['description']
                item['gender'] = user['gender']
                item['mbtype'] = user['mbtype']
                item['urank'] = user['urank']
                item['mbrank'] = user['mbrank']
                item['followers_count'] = user['followers_count']
                item['follow_count'] = user['follow_count']
                item['cover_image_phone'] = user['cover_image_phone']
                item['avatar_hd'] = user['avatar_hd']
                try:
                    item['badge'] = len(user['badge'])
                except:
                    item['badge'] = 0
                yield item
        except:
            print('no data')
        if self.comment_page < 100000:
            headers = {
                'USER_AGENT': random.choice(self.user_agent)
            }
            try:
                max_id = str(html['data']['max_id'])
                max_id_type = str(html['data']['max_id_type'])
                next_url = self.start_url.format(weibo_id, weibo_id,max_id_type) + '&max_id='+ max_id
                if self.comment_page%50==10:
                    time.sleep(100)
                yield scrapy.Request(url=next_url, callback=self.parse_comment, headers=headers,
                                         cookies=self.settings['COOKIES'],
                                         meta={'weibo_id': self.id})  # , 'proxy': 'https://{}'.format(self.proxy)
            except:
                print("无数据")

                # self.proxy = random.choice(self.proxy_list)

