# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
from  Music.items import MusicItem

class Qq3Spider(scrapy.Spider):
    name = 'qq3'
    allowed_domains = ['qq.com']
    def start_requests(self):
        base_url='https://c.y.qq.com/v8/fcg-bin/getmv_by_tag?g_tk=5381&type=2&pageno={}&pagecount=20'
        urls = [base_url.format(str(i)) for i in range(61087)]
        for url in urls[31087:]:
            yield Request(url,callback=self.parse)
    def parse(self, response):
        item=MusicItem()
        item['type']='MV名'
        rsp = response.text.replace('MusicJsonCallback(','')[:-1]
        datas=json.loads(rsp)['data']['mvlist']
        for data in datas:
            item['mvtitle']=data['mvtitle']
            item['singername']=data["singername"]
            yield item

