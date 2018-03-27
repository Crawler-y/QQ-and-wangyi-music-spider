# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib import request
import json
import re
from Music.items import MusicItem


#通过&sin&ein进行翻页操作
class Qq2Spider(scrapy.Spider):
    name = 'qq2'
    allowed_domains = ['qq.com']
    # start_urls = ['https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg?picmid=1&rnd=0.3260375025962392&g_tk=5381&jsonpCallback=getPlaylist&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&categoryId=10000000&sortId=5&sin=120&ein=149']
    def start_requests(self):
        headers = {
            ':authority':'c.y.qq.com',
            ':method':'GET',
            ':path':'/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg?picmid=1&rnd=0.3260375025962392&g_tk=5381&jsonpCallback=getPlaylist&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&categoryId=10000000&sortId=5&sin=120&ein=149',
            ':scheme':'https',
            'accept':'*/*',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.9',
            'cookie':'pgv_pvi=5176126464; pt2gguin=o0584048511; RK=of7kNI+kf1; ptcz=0ec0f931f571b60a2771f02e44c751c0adb4c5a2602778baf6545865c70bc2be;  pgv_pvid=7752824365; eas_sid=31H5h1o5M7P3V123K8g8X4W182; ts_uid=3405668406; pgv_info=ssid=s5995755898; ts_refer=www.google.com.hk/; pgv_si=s5935997952; yqq_stat=0; ts_last=y.qq.com/portal/playlist.html',
            'referer':'https://y.qq.com/portal/playlist.html',
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }

        st_url='https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg?picmid=1&rnd=0.3260375025962392&g_tk=5381&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&categoryId=10000000&sortId=5&sin=5760&ein=5789'
        yield Request(url=st_url,headers=headers, callback=self.parse)
    def parse(self, response):
        pre_url=response.url
        rsp=response.text.replace('MusicJsonCallback(','')[:-1]
        datas=json.loads(rsp)['data']['list']
        item=MusicItem()
        item['type']='歌单'
        for i in datas:
            item['dissname']=i['dissname']
            item['name']=i['creator']['name'].strip()
            print(item)
            yield item
        next_num =int(request.unquote(re.search(r'&sin=(.*?)&ein',pre_url).group(1)))+30
        next_ein = next_num+29
        next_url='https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg?picmid=1&rnd=0.3260375025962392&g_tk=5381&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&categoryId=10000000&sortId=5&sin='+str(next_num)+'&ein='+str(next_ein)
        while bool(datas):
            yield Request(next_url,callback=self.parse)
        print('该分类的数据已完成')