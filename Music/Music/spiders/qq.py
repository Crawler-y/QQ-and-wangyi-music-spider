# -*- coding: utf-8 -*-
import scrapy
import json
import re
from urllib import request
from scrapy import Request
from Music.items import MusicItem

#https://y.qq.com/portal/album_lib.html#sin=58800(1940*20)
class QqSpider(scrapy.Spider):
    name = 'qq'
    allowed_domains = ['qq.com']
    def start_requests(self):
        base_url='https://u.y.qq.com/cgi-bin/musicu.fcg?g_tk=5381&jsonpCallback=getUCGI7130691201634769&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22albumlib%22%3A%7B%22method%22%3A%22get_album_by_tags%22%2C%22param%22%3A%7B%22area%22%3A4%2C%22company%22%3A-1%2C%22genre%22%3A-1%2C%22type%22%3A-1%2C%22year%22%3A-1%2C%22sort%22%3A2%2C%22get_tags%22%3A1%2C%22sin%22%3A6820%2C%22num%22%3A20%2C%22click_albumid%22%3A0%7D%2C%22module%22%3A%22music.web_album_library%22%7D%7D'
        yield Request(url=base_url,callback=self.parse)

    def parse(self, response):
        item=MusicItem()
        item['type']='专辑'
        # area_list=['4','14','15','3','0']
        # area=area_list.pop()
        rsq_url=response.url
        url_area=re.search(r'area%22%3A(.*?)%2C',rsq_url).group(1)
        if url_area == '1':
            item['area'] = '内地'
        elif url_area == '0':
            item['area'] = '港台'
        elif url_area == '3':
            item['area']='欧美'
        elif url_area == '15':
            item['area'] = '韩国'
        elif url_area == '14':
            item['area'] = '日本'
        elif url_area == '4':
            item['area'] = '其他'
        dict_dat=json.loads(response.text)
        dat_nodes=dict_dat["albumlib"]['data']['list']
        for node in dat_nodes:
            item['album']=node["album_name"]
            yield item
        next_num=int(request.unquote(re.search(r'sin%22%3A(.*?)%2C',rsq_url).group(1)))+20
        #
        next_url='https://u.y.qq.com/cgi-bin/musicu.fcg?&g_tk=5381&jsonpCallback=getUCGI40028220795882663&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22albumlib%22%3A%7B%22method%22%3A%22get_album_by_tags%22%2C%22param%22%3A%7B%22area%22%3A4%2C%22company%22%3A-1%2C%22genre%22%3A-1%2C%22type%22%3A-1%2C%22year%22%3A-1%2C%22sort%22%3A2%2C%22get_tags%22%3A1%2C%22sin%22%3A'+str(next_num)+'%2C%22num%22%3A20%2C%22click_albumid%22%3A0%7D%2C%22module%22%3A%22music.web_album_library%22%7D%7D'
        while bool(dat_nodes):
            yield Request(next_url,callback=self.parse)
        # next_purl=next_url.replace(re.search(r'area%22%3A(.*?)%2C',rsq_url).group(1),area)
        print('进入下个主题数据',area)
        # yield Request(next_purl,callback=self.parse)