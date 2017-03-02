# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CzbbsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 开班典礼
class HeimaKbdlItem(scrapy.Item):
    bankuai_name = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    updateTime = scrapy.Field()
    sawNum = scrapy.Field()
    replyNum = scrapy.Field()
    lastReplyAuthor = scrapy.Field()
    lastReplyTime = scrapy.Field()
    href = scrapy.Field()


class HeimaKbdlDetailItem(scrapy.Item):
    bankuai_name = scrapy.Field()
    copy_url = scrapy.Field()
    topsticks = scrapy.Field(serializer=str)
    floor_level = scrapy.Field()
    title = scrapy.Field()
    replyNum = scrapy.Field()
    sawNum = scrapy.Field()
    updateTime = scrapy.Field()


class HeimaKbdlDetailPassenerItem(scrapy.Item):
    title = scrapy.Field()
    username = scrapy.Field()
    replyTime = scrapy.Field()
    replyContent = scrapy.Field()
