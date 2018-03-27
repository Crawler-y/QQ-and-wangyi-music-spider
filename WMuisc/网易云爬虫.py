
#'http://music.163.com/discover/playlist'
import requests
from lxml import etree
import openpyxl
from openpyxl.compat import range
import os

class Spider(object):
    def downloader(self,i):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
        headers = {'User-Agent': user_agent,
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate',
                    'Accept-Language':'zh-CN,zh;q=0.9',
                    'Cookie':'_ntes_nnid=4d8ad324d24c59eb6da7051a0a05fc5e,1515553940076; _ntes_nuid=4d8ad324d24c59eb6da7051a0a05fc5e; nts_mail_user=17520467637@163.com:-1:1; _iuqxldmzr_=32; mail_psc_fingerprint=82f2e87332bd4110ed2a44054fcfb5ac; __e_=1516247005297; _ngd_tid=OnFo4qYXlC4Y0HQNtDRFdaHkp7hDs%2BH8; starttime=; NTES_SESS=v_vaTD33QcJmqsk9xMBqy3JiQ6hfil81WniUgOeM3WpcqC5iqgFBt65tVHO6KVINwyVBAj38Jsy5jz8u6_MF2f9J7Sv3cJcI_6Pgv6r3QfY2a1kVKj_wBvqmeZy6qGDZPQQeaVjv_AINs9NzTwBAD0CZC78NTG.bfM0TI6EjJTHwtQTtyzKieOnE7iSX18gUqL4o48_hRDVslFhaTKjZD1wrU; S_INFO=1519793416|0|3&80##|m17520467637; P_INFO=m17520467637@163.com|1519793416|0|mail163|00&99|gud&1518424388&mail163#gud&440100#10#0#0|175637&1||17520467637@163.com; df=mail163_letter; MUSIC_EMAIL_U=da136b3e28e1ffea08f0dfa3be1d72755053be85f4706fa6fdac9ea330a9cc49e11bc961639315dac924348eecb6f69e249a51a7d0a9515af2f513a9c38b5dc7; playliststatus=visible; __utmc=94650624; __utma=94650624.2039085753.1519607318.1519805862.1519809365.5; __utmz=94650624.1519809365.5.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; JSESSIONID-WYYY=VHtsC9GlAaWbKH2eTcdAd91DM8%5CQ8d2e%2BlpGxzfpiwwZNi6M99UhWJfNSJc16AkjdsHKdBhlKIo%2B0CDn708eEfKFjxDzzDjsCUEiWeEdvNVdqqUo%2FiQq4aA%5CWzJro6q5y7YRtF6uOi95KUCHOKIQUIi%2F5TrY2rl%5C9sZHVgJzCOMVvrPh%3A1519811338731; __utmb=94650624.14.10.1519809365',
        'Host':'music.163.com',
        'Referer':'http://music.163.com/',
                   }
        # 使用offset来控制翻页
        params = {
            'order':'hot',
            'cat':'全部',
            'limit':'35',
            'offset':i
        }
        url1='http://music.163.com/discover/playlist/'
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
    # 作者xpath//ul[@id="m-pl-container"]/li/p[2]/a/text()
    # 歌名xpathxpath//ul[@id="m-pl-container"]/li/p[1]/a/text()
    def parse(self,html):
        # 解析完成返回需求数据
        print('对请求数据进行解析')
        #当解析出的数据为空的时候
        rsp=etree.HTML(html)
        datas=rsp.xpath('//ul[@id="m-pl-container"]/li')
        data_list=[]
        for i in datas:
            music_names=i.xpath('./p[1]/a/text()')[0]
            users=i.xpath('./p[2]/a/text()')[0]
            lines=[music_names,users]
            data_list.append(lines)
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
            dest_filename = '网易云歌单.xlsx'
            wj = openpyxl.load_workbook(dest_filename)
            activsheet = wj.get_active_sheet()
            activsheet.append(lines)
            wj.save(dest_filename)
        print('存档完成')

    # 定义调度器
    def run(self,i):
        pages=self.downloader(i)
        if type(pages) is str:
            #进行后续的解析工作
            print('数据请求成功')
            data_list=self.parse(pages)
            self.save(data_list)

        elif type(pages) is tuple:
            #生成文件写入错误的url
            with open('erro.txt','a')as f:
                f.writelines('\n'+str(pages))

spider=Spider()
offset_list=[str(i) for i in range(0,1226,35)]
for i in offset_list:
    spider.run(i)