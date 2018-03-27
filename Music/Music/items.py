# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MusicItem(scrapy.Item):
    album=scrapy.Field()
    area=scrapy.Field()
    dissname=scrapy.Field()
    name=scrapy.Field()
    type=scrapy.Field()
    mvtitle=scrapy.Field()
    singername=scrapy.Field()