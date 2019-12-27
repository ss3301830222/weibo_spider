# -*- coding: utf-8 -*-
import scrapy
from fans.items import StarInfoItem
from fans.items import WeiboInfoItem
from fans.items import RepostItem
from fans.items import CommentItem
from fans.items import AttitudeItem
import time
import json
import random
import logging
import requests


class GetallSpider(scrapy.Spider):
    name = 'getall'
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
    def __init__(self,*args,**kwargs):
        super(GetallSpider, self).__init__(*args, **kwargs)
        # [1846360445, 2734343924, 1814284757, 1609648201, 5934019851, 2193518494, 3432945104]体育
        self.id_list = ['1968758563','1549362863','5391793730','1780449083','1280761142','7262819693','1720664360','1434004434','1701580461','1695958733']
        self.cookie_url = 'http://127.0.0.1:5000/weibo/random'
        self.cookie = json.loads(requests.get(self.cookie_url).text)
        self.weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={}&t=0&type=uid&value={}&containerid={}&page={}'
        self.weibo_page_max = 3
        self.repost_url = 'https://m.weibo.cn/api/statuses/repostTimeline?id={}&page={}'
        self.repost_max = 100
        self.comment_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type={}'
        self.comment_max = 50  # 最多获取多少页评论
        self.attitude_url = 'https://m.weibo.cn/api/attitudes/show?id={}&page={}'
        self.attitude_max = 11

    def start_requests(self):
        for id in self.id_list:
            start_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}'.format(id)
            logging.warning(id)
            yield scrapy.Request(url=start_url, callback=self.parse_starinfo,meta={'id':id})

    def parse_starinfo(self, response):
        id = response.meta['id']
        logging.warning("开始获取博主{}基本信息".format(id))
        item_starinfo = StarInfoItem()
        html = response.text
        html = json.loads(html)
        item_starinfo['id'] = str(html['data']['userInfo']['id'])
        item_starinfo['screen_name'] = html['data']['userInfo']['screen_name']
        item_starinfo['profile_url'] = html['data']['userInfo']['profile_url']
        item_starinfo['statuses_count'] = str(html['data']['userInfo']['statuses_count'])
        item_starinfo['verified_reason'] = html['data']['userInfo']['verified_reason']
        item_starinfo['gender'] = html['data']['userInfo']['gender']
        item_starinfo['mbtype'] = str(html['data']['userInfo']['mbtype'])
        item_starinfo['urank'] = str(html['data']['userInfo']['urank'])
        item_starinfo['mbrank'] = str(html['data']['userInfo']['mbrank'])
        item_starinfo['followers_count'] = str(html['data']['userInfo']['followers_count'])
        item_starinfo['follow_count'] = str(html['data']['userInfo']['follow_count'])
        item_starinfo['weibo_containerid'] = str(html['data']['tabsInfo']['tabs'][1]['containerid'])
        yield item_starinfo
        logging.warning("博主{}基本信息获取完毕".format(id))
        weibo_url = self.weibo_url.format(id,id,item_starinfo['weibo_containerid'],'{}')
        logging.warning(id)
        yield scrapy.Request(url=weibo_url.format(1),headers=self.headers,callback=self.parse_weibo, meta={'weibo_page':1,'weibo_url':weibo_url,'star_id':id})

    def parse_weibo(self, response):
        item = WeiboInfoItem()
        star_id = response.meta['star_id']
        weibo_page = response.meta['weibo_page']
        weibo_url = response.meta['weibo_url']
        logging.warning("开始获取博主{}第{}页微博数据".format(star_id,weibo_page))
        # try:
        data = response.text
        content = json.loads(data).get('data')
        cards = content.get('cards')
        if (len(cards) > 0):
            i = 1
            for j in range(len(cards)):
                card_type = cards[j].get('card_type')
                if (card_type == 9):
                    logging.warning("开始获取第{}页第{}条微博数据".format(weibo_page,i))
                    item['scheme'] = cards[j].get('scheme')
                    mblog = cards[j].get('mblog')
                    item['star_id'] = mblog.get('user').get('id')
                    item['weibo_id'] = mblog.get('id')
                    item['weibo_text'] = mblog.get('raw_text')
                    item['attitudes_count'] = mblog.get('attitudes_count')
                    item['comments_count'] = mblog.get('comments_count')
                    item['created_at'] = mblog.get('created_at')
                    item['reposts_count'] = mblog.get('reposts_count')
                    item['text'] = mblog.get('text')
                    yield item

                    logging.warning("％％第{}页第{}条转发数据开始获取％％".format(weibo_page, i))
                    yield scrapy.Request(url=self.repost_url.format(item['weibo_id'], 1),cookies=json.loads(requests.get(self.cookie_url).text),
                                         callback=self.parse_repost, meta={'weibo_id': item['weibo_id'],
                                                                           'weibo_page':weibo_page,
                                                                           'weibo_i':i,
                                                                           'n':1,
                                                                           'star_id':item['star_id']})

                    logging.warning("％％第{}页第{}条评论数据开始获取％％".format(weibo_page,i))
                    yield scrapy.Request(url=self.comment_url.format(item['weibo_id'],item['weibo_id'],0),
                                         callback=self.parse_comment, meta={'weibo_id': item['weibo_id'],
                                                                            'weibo_page': weibo_page,
                                                                            'weibo_i': i,
                                                                            'n':1,
                                                                            'star_id': item['star_id']},
                                         cookies=json.loads(requests.get(self.cookie_url).text),
                                         headers=self.headers)

                    logging.warning("％％第{}页第{}条点赞数据开始获取％％".format(weibo_page, i))
                    yield scrapy.Request(url=self.attitude_url.format(item['weibo_id'],1),
                                         cookies=json.loads(requests.get(self.cookie_url).text),headers=self.headers,
                                         callback=self.parse_attitude,
                                         meta={'weibo_id': item['weibo_id'],'weibo_page':weibo_page,'weibo_i':i,'n':1,
                                               'star_id': item['star_id']})

                    logging.warning("第{}页第{}条微博数据获取完毕".format(weibo_page, i))
                    i += 1
        else:
            logging.warning("第{}页无有效微博数据")
        # except Exception as e:
        #     logging.warning("第{}页微博无数据".format(self.weibo_page))
        if weibo_page<self.weibo_page_max:
            weibo_page += 1
            yield scrapy.Request(url=weibo_url.format(weibo_page), headers=self.headers, callback=self.parse_weibo,
                                 meta={'weibo_page':weibo_page,'weibo_url':weibo_url,'star_id':star_id})
        else:
            logging.warning("此次微博数据获取完毕")

    def parse_repost(self, response):
        weibo_i = response.meta['weibo_i']
        weibo_page = response.meta['weibo_page']
        weibo_id = response.meta['weibo_id']
        star_id = response.meta['star_id']
        html = response.text
        html = json.loads(html)
        repost_max = html['data']['max']
        logging.warning('第{}页第{}条微博转发页数为{}'.format(weibo_page,weibo_i,repost_max))
        repost_max = min(self.repost_max,repost_max)
        try:
            for k in range(1,repost_max+1):
                next_url = self.repost_url.format(weibo_id, k)
                yield scrapy.Request(url=next_url, callback=self.parse_repost_detail, headers=self.headers,
                                     meta={'weibo_id': weibo_id,'star_id': star_id},
                                     cookies=json.loads(requests.get(self.cookie_url).text))
                if k % 10 == 5:
                    logging.warning("转发更换cookies")
                    self.cookie = json.loads(requests.get(self.cookie_url).text)
            if k == repost_max:
                logging.warning("**第{}页第{}条转发数据获取完毕**".format(weibo_page, weibo_i))
        except:
            logging.warning("**第{}页第{}条转发数据有错误**".format(weibo_page, weibo_i))

    def parse_repost_detail(self, response):
        weibo_id = response.meta['weibo_id']
        html = response.text
        html = json.loads(html)
        # try:
        for i in range(len(html['data']['data'])):
            item = RepostItem()
            item['star_id'] = response.meta['star_id']
            item['star_weibo_id'] = weibo_id
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
        # except:
        #     logging.warning("本页无数据")

    def parse_comment(self, response):
        weibo_id = response.meta['weibo_id']
        weibo_i = response.meta['weibo_i']
        weibo_page = response.meta['weibo_page']
        star_id = response.meta['star_id']
        n = response.meta['n']
        html = response.text
        try:
            html = json.loads(html)
            comment_max = html['data']['max']
            comment_max = min(self.comment_max, comment_max)
            data = html['data']['data']
            for i in range(len(data)):
                item = CommentItem()
                item['star_id'] = star_id
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
            n += 1
            if n % 20 == 10:
                self.cookie = json.loads(requests.get(self.cookie_url).text)
                logging.warning(n)
            if n < comment_max:
                max_id = str(html['data']['max_id'])
                max_id_type = str(html['data']['max_id_type'])
                next_url = self.comment_url.format(weibo_id, weibo_id, max_id_type) + '&max_id=' + max_id
                yield scrapy.Request(url=next_url, callback=self.parse_comment, headers=self.headers,
                                     meta={'weibo_id': weibo_id, 'weibo_i': weibo_i, 'weibo_page': weibo_page,'n':n,'star_id':star_id},
                                     cookies=self.cookie)
            else:
                logging.warning("％％第{}页第{}条评论数据获取完毕％％".format(weibo_page, weibo_i))
        except:
            logging.warning("该页无评论数据")

    def parse_attitude(self, response):
        weibo_id = response.meta['weibo_id']
        weibo_i = response.meta['weibo_i']
        weibo_page = response.meta['weibo_page']
        star_id = response.meta['star_id']
        n = response.meta['n']
        html = response.text
        html = json.loads(html)
        # try:
        data = html['data']['data']
        total_number = html['data']['total_number']
        for i in range(len(data)):
            item = AttitudeItem()
            item['star_id'] = star_id
            item['star_weibo_id'] = weibo_id
            item['total_number'] = total_number
            item['attitude_id'] = data[i]['id']#此条赞的ｉｄ
            item['created_at'] = data[i]['created_at']
            item['source'] = data[i]['source']
            user = data[i]['user']
            item['id'] = user['id']
            item['screen_name'] = user['screen_name']
            item['profile_image_url'] = user['profile_image_url']
            item['verified'] = user['verified']
            item['followers_count'] = user['followers_count']
            item['mbtype'] = user['mbtype']
            item['profile_url'] = user['profile_url']
            yield item
        # except:
        #     logging.warning("点赞不存在")
        n += 1
        next_url = self.attitude_url.format(weibo_id, n)
        logging.warning(n)
        if n%10==5:
            self.cookie = json.loads(requests.get(self.cookie_url).text)
            logging.warning("点赞更换cookie")
        if 50*n < min(total_number,50*self.attitude_max):
            yield scrapy.Request(url=next_url, callback=self.parse_attitude, headers=self.headers,cookies=self.cookie,
                                 meta={'weibo_id': weibo_id, 'weibo_page': weibo_page, 'weibo_i': weibo_i,'n':n,'star_id':star_id})
            logging.warning('下一页')