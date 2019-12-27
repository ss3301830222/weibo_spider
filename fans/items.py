# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StarInfoItem(scrapy.Item):
    id = scrapy.Field()
    screen_name = scrapy.Field()
    profile_url = scrapy.Field()
    statuses_count = scrapy.Field()
    verified_reason = scrapy.Field()
    gender = scrapy.Field()
    mbtype = scrapy.Field()
    urank = scrapy.Field()
    mbrank = scrapy.Field()
    followers_count = scrapy.Field()
    follow_count = scrapy.Field()
    # 有多个containerid，包括主页，微博，超话，相册等，这里暂时只取微博
    weibo_containerid= scrapy.Field()

class WeiboInfoItem(scrapy.Item):
    scheme = scrapy.Field()
    star_id = scrapy.Field()
    weibo_id = scrapy.Field()
    weibo_text = scrapy.Field()
    attitudes_count = scrapy.Field()
    comments_count = scrapy.Field()
    created_at = scrapy.Field()
    reposts_count = scrapy.Field()
    text = scrapy.Field()

class RepostItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_screen_name = scrapy.Field()
    gender = scrapy.Field()
    followers_count = scrapy.Field()
    follow_count = scrapy.Field()
    created_at = scrapy.Field()
    source = scrapy.Field()
    statuses_count = scrapy.Field()
    id = scrapy.Field()
    urank = scrapy.Field()
    mbrank = scrapy.Field()
    description = scrapy.Field()
    badge = scrapy.Field()
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    attitudes_count = scrapy.Field()
    raw_text = scrapy.Field()
    repost_id = scrapy.Field()
    pending_approval_count = scrapy.Field()
    isLongText = scrapy.Field()
    cover_image_phone = scrapy.Field()
    avatar_hd = scrapy.Field()
    mbtype = scrapy.Field()
    verified = scrapy.Field()
    profile_url = scrapy.Field()
    star_weibo_id = scrapy.Field()
    star_id = scrapy.Field()

class CommentItem(scrapy.Item):
    star_weibo_id = scrapy.Field()
    created_at = scrapy.Field()
    comment_id = scrapy.Field()
    floor_number = scrapy.Field()
    text = scrapy.Field()
    total_number = scrapy.Field()
    isLikedByMblogAuthor = scrapy.Field()
    like_count = scrapy.Field()
    #用户信息
    id = scrapy.Field()
    screen_name = scrapy.Field()
    profile_image_url = scrapy.Field()
    profile_url = scrapy.Field()
    statuses_count = scrapy.Field()
    verified = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    mbtype = scrapy.Field()
    urank = scrapy.Field()
    mbrank = scrapy.Field()
    followers_count = scrapy.Field()
    follow_count = scrapy.Field()
    cover_image_phone = scrapy.Field()
    avatar_hd = scrapy.Field()
    badge = scrapy.Field()
    star_id = scrapy.Field()

class AttitudeItem(scrapy.Item):
    star_weibo_id = scrapy.Field()
    total_number = scrapy.Field()
    attitude_id = scrapy.Field()
    created_at = scrapy.Field()
    source = scrapy.Field()
    id = scrapy.Field()
    screen_name = scrapy.Field()
    profile_image_url = scrapy.Field()
    verified = scrapy.Field()
    followers_count = scrapy.Field()
    mbtype = scrapy.Field()
    profile_url = scrapy.Field()
    star_id = scrapy.Field()

