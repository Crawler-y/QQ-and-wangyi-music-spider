# # -*- coding: utf-8 -*-
#
# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# size=os.path.getsize('D:\My Documents\Desktop\qq音乐MV2.xlsx')
# size /= (1024*1024)
# import openpyxl
import os
# from openpyxl.compat import range


class MusicPipeline(object):

    def process_item(self, item, spider):
        if item['type'] =='专辑':
            os.chdir('D:\My Documents\Desktop\Music/')
            dest_filename = 'qq音乐专辑.xlsx'
            wj = openpyxl.load_workbook(dest_filename)  # 打开excel
            activsheet = wj.get_active_sheet()
            line = [item['album'],item['area']]
            activsheet.append(line)
            wj.save(dest_filename)
        elif item['type'] == '歌单':
            os.chdir('D:\My Documents\Desktop\Music/')
            dest_filename = 'qq音乐歌单.xlsx'
            wj = openpyxl.load_workbook(dest_filename)  # 打开excel
            activsheet = wj.get_active_sheet()
            line = [item['dissname'],item['name']]
            activsheet.append(line)
            wj.save(dest_filename)
        elif item['type'] == 'MV名':
            os.chdir('D:\My Documents\Desktop\Music/')
            # dest_filename = 'qq音乐MV.xlsx'
            # wj = openpyxl.load_workbook(dest_filename)  # 打开excel
            # activsheet = wj.get_active_sheet()
            # line = [ item['mvtitle'],item['singername']]
            # activsheet.append(line)
            # wj.save(dest_filename)
            with open('MV名.txt','a',encoding='utf-8')as f:
                f.writelines(item['mvtitle']+'\n')
            with open('歌手名.txt','a',encoding='utf-8')as f2:
                f2.writelines(item['singername']+'\n')
        return item



