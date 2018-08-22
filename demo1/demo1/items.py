# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Demo1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 电影海报
    post = scrapy.Field()
    # 电影名字
    name = scrapy.Field()
    # 豆瓣评分
    score = scrapy.Field()
    # 电影类型
    _type = scrapy.Field()

    # 导演
    director = scrapy.Field()
    # 编剧
    editor = scrapy.Field()
    # 主演
    actor = scrapy.Field()
    # 片长
    long_time = scrapy.Field()
    # 介绍
    introduce = scrapy.Field()
