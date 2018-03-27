
#'http://music.163.com/discover/playlist'
import requests
from lxml import etree
import openpyxl
from openpyxl.compat import range
# from gevent import monkey; monkey.patch_all()
# from gevent.pool import Pool
import os

class Spider(object):
    def downloader(self,id,i):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        headers  = {'User-Agent': user_agent,
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate',
                    'Accept-Language':'zh-CN,zh;q=0.9',
                    'Cookie':'_ntes_nnid=4d8ad324d24c59eb6da7051a0a05fc5e,1515553940076; _ntes_nuid=4d8ad324d24c59eb6da7051a0a05fc5e; nts_mail_user=17520467637@163.com:-1:1; _iuqxldmzr_=32; mail_psc_fingerprint=82f2e87332bd4110ed2a44054fcfb5ac; __e_=1516247005297; _ngd_tid=OnFo4qYXlC4Y0HQNtDRFdaHkp7hDs%2BH8; __utmz=94650624.1519809365.5.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; P_INFO=m17520467637@163.com|1519883564|0|mail163|00&99|gud&1519812184&mail163#gud&440100#10#0#0|175637&1|mail163|17520467637@163.com; __utmc=94650624; __utma=94650624.2039085753.1519607318.1519885886.1519892814.8; JSESSIONID-WYYY=hBgNkzdutIlAQbkWas6PiguzGYPPPPlW5MBx56MTtBKcPOY7nUdQJ%2Fb5mIjG9nPFrOfAajiujm0G%5CgyYCeSrZFAJJBK%2FIBwJ%5CIIbCVB%2FJNbh4ZO84HsOTzqfDsaE%2BK4ricrTZj1e0DyYohHoXr9wZzedVPFCaiylWFB%5CP%5CZ%2BGJay1IH8%3A1519896389103; __utmb=94650624.29.10.1519892814',
                    'Host':'music.163.com',
                    'Upgrade-Insecure-Requests':'1',
                    'Referer':'http://music.163.com/',
                   }
        # 使用offset来控制翻页
        params = {
            'id':id,
            'order':'12',
            '_hash':'allradios',
            'limit':'30',
            'offset':i,
        }
        url1='http://music.163.com/discover/djradio/category'
        sess = requests.session()
        r = sess.get(url=url1, headers=headers, params=params, allow_redirects=False)
        if r.status_code == 200 :
            #爬取正常进入解析提取数据
            return r.text
        else:
            #出现异常进行log记录
            status=r.status_code
            erro_url=r.url
            return status,erro_url
    # 类别//div[@id="id-category-box"]/div[1]/ul[1]/li[1]/a/em
    def parse(self,html,title):
        # 解析完成返回需求数据
        print('对请求数据进行解析')
        #当解析出的数据为空的时候
        rsp=etree.HTML(html)
        datas=rsp.xpath('//*[@id="allradios"]/ul/li')
        data_list=[]
        for i in datas:
            Mv_names=i.xpath('./div/h3/a/text()')[0]
            users=i.xpath('./div/p[1]/a/text()')[0]
            lines=[Mv_names,users,title]
            data_list.append(lines)
        print(data_list)
        return data_list
        #当作者名不存在或者数据不存在的时候需要写入错误日志

    def erro(self,status,url):
        pass

    # 定义函数进行数据保存
    def save(self,data_list):
        for lines in data_list:
            # datas的样式传入[xx,xx]
            # 当存档出错的时候
            os.chdir('D:\My Documents\Desktop\WMuisc/')
            dest_filename = '网易云电台.xlsx'
            try:
                wj = openpyxl.load_workbook(dest_filename)
            except Exception as e2:
                print(e2)
            activsheet = wj.get_active_sheet()
            activsheet.append(lines)
            try:
                wj.save(dest_filename)
            except Exception as e:
                print(e)
        print('存档完成')

    # 定义调度器
    def run(self,id,i,title):
        pages=self.downloader(id,i)
        if type(pages) is str:
            #进行后续的解析工作
            print('数据请求成功')
            data_list=self.parse(pages,title)
            self.save(data_list)
        elif type(pages) is tuple:
            #生成文件写入错误的url
            print('出现错误！！！')
            with open('erro.txt','a')as f:
                f.writelines('\n'+str(pages))
    def tmp(self):
        tm=[['有声书','10001',1200],['知识技能','453050',1200],['商业财经','453051',390],['人文历史','11',1200],['外语世界','13',1200],['亲子宝贝','14',1200],['创作|翻唱','2001',1200],['音乐故事','2',1200],['3D|电子','10002',1200],['相声曲艺','8',780],['情感调频','3',1200],['美文读物','6',1200],['脱口秀','5',1200],['广播剧','7',1200],['二次元','3001',1200],['明星做主播','1',90],['娱乐影视','4',1200],['科技科学','453052',210],['校园教育','4001',1200],['旅途城市','12',1200]]
        return tm

spider=Spider()
tmps=spider.tmp()
for j in tmps:
    title=j[0]
    id=j[1]
    sum=j[2]
    offset_list=[str(i) for i in range(0,sum,30)]
    for i in offset_list:
       spider.run(id,i,title)
print('大功告成')
# 协程爬虫
# greenlets=[gevent.spawn(spider.run,str(i)) for i in range(0,1200,30) ]
# gevent.joinall(greenlets)
#协程池
# pool=Pool(16)
# results=pool.map(spider.run,offset_list)