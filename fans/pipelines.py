# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import csv
from fans.items import RepostItem
from fans.items import StarInfoItem
from fans.items import WeiboInfoItem
from fans.items import CommentItem
from fans.items import AttitudeItem
import os

class FansPipeline(object):

    name = "name"
    dirs = "dirs"
    def process_item(self, item, spider):

        if isinstance(item, StarInfoItem):
            self.name = item['screen_name']
            self.dirs = "/home/xiayu-ubuntu/桌面/bbbb_spider/Reptile-master/微博/fans"+"/"+"明星微博"+'/'
            if not os.path.exists(self.dirs):
                os.makedirs(self.dirs)
            file = self.dirs + str(item['id']) + item['screen_name'] + '基本信息.txt'
            with open(file,'a+') as f:
                f.write('明星id：'+item['id']+'\n'+'名称：'+item['screen_name']+'\n'+'主页：'+item['profile_url']+'\n'+
                        '发博次数：'+item['statuses_count']+'\n'+'认证理由：'+item['verified_reason']+'\n'+'性别：'+
                        item['gender']+'\n'+'粉丝数：'+item['followers_count']+'\n'+'关注数：'+item['follow_count']+'\n'+
                        '用户等级：'+item['urank']+'\n'+'mbtype(是否超ｖ１)：'+item['mbtype']+'\n'+'mbrank(是否超ｖ２)：'+
                        item['mbrank']+'\n'+'微博内容地址：'+item['weibo_containerid']+'\n')
            return item

        if isinstance(item, WeiboInfoItem):
            file =  self.dirs + str(item['star_id']) +'微博信息.csv'
            with open(file,'a') as f:
                csvwriter = csv.writer(f, dialect=("excel"))
                csvwriter.writerow((item['scheme'], item['star_id'], item['weibo_id'],item['weibo_text'],
                                    item['attitudes_count'],item['comments_count'],item['created_at'],item['reposts_count'],item['text']
                                    ))
            return item

        if isinstance(item, RepostItem):
            file =  self.dirs + str(item['star_id']) + '转发'+'.csv'
            with open(file,'a+') as f:
                csvwriter = csv.writer(f, dialect=("excel"))
                csvwriter.writerow(
                    (item['user_screen_name'], item['gender'], item['followers_count'],item['follow_count'],
                    item['created_at'],item['source'],item['statuses_count'],item['id'],item['urank'],
                    item['mbrank'],item['description'],item['badge'],item['reposts_count'],
                    item['comments_count'],item['attitudes_count'],item['raw_text'],item['repost_id'],
                    item['pending_approval_count'],item['isLongText'],item['cover_image_phone'],item['avatar_hd'],
                    item['mbtype'],item['verified'],item['profile_url'],item['star_weibo_id']))
            return item

        if isinstance(item, CommentItem):
            file =  self.dirs + str(item['star_id']) + '评论'+'.csv'
            with open(file, 'a+') as f:
                csvwriter = csv.writer(f, dialect=("excel"))
                csvwriter.writerow(
                    (item['created_at'],item['comment_id'],item['floor_number'],item['text'],item['total_number'],
                     item['isLikedByMblogAuthor'],item['like_count'],item['id'],item['screen_name'],item['profile_image_url'],
                     item['profile_url'],item['statuses_count'],item['verified'],item['description'],item['gender'],
                     item['mbtype'],item['urank'],item['mbrank'],item['followers_count'],item['follow_count'],item['cover_image_phone'],
                     item['avatar_hd'],item['badge'],item['star_weibo_id']))
            return item

        if isinstance(item, AttitudeItem):
            file =  self.dirs + str(item['star_id']) + '点赞'+'.csv'
            with open(file, 'a+') as f:
                csvwriter = csv.writer(f, dialect=("excel"))
                csvwriter.writerow(
                    (item['total_number'],item['attitude_id'],item['created_at'],item['source'],item['id'],item['screen_name'],
                     item['profile_image_url'],item['verified'],item['followers_count'],item['mbtype'],item['profile_url'],item['star_weibo_id']))
            return item
