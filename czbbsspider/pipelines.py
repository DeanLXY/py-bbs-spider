# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import requests
from czbbsspider import settings
import os

from czbbsspider.items import HeimaKbdlItem, HeimaKbdlDetailItem
from openpyxl import Workbook, load_workbook

import datetime
import re


class CzbbsspiderPipeline(object):

    def process_item(self, item, spider):
        return item


class FilterWordsPipeline(object):

    def __init__(self):
        # self.file = open("data.json", "wb")
        print '\n'+'FilterWordsPipeline 正在初始化'
        self.file = codecs.open(
            "scraped_data_utf8.json", "wb", encoding="utf-8")

    def process_item(self, item, spider):
        if item:
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(line)
            return item

    def spider_closed(self, spider):
        self.file.close()


# 过滤正文信息
class FilterTitlePipeLine(object):

    def process_item(self, item, spider):
        if isinstance(item, HeimaKbdlItem):
            if item['title']:
                return item
            else:
                # raise Exception(u'不是正文信息，自动忽略')
                pass
        else:
            return item


data_dic = {}

# 匹配账号信息


class ReadAccountPipeline(object):

    def __init__(self):
        data_dic.clear()
        workbook_ = load_workbook(filename='bbsaccount.xlsx')
        sheetnames = workbook_.get_sheet_names()  # 获得表单名字
        self.ws = workbook_.get_sheet_by_name(sheetnames[0])  # 从工作表中提取某一表单

        # 把数据存到字典中 d = {“论坛名字”:"真实名字"}
        for rx in range(2, self.ws.max_row + 1):
            w2 = self.ws.cell(row=rx, column=2).value
            w4 = self.ws.cell(row=rx, column=4).value
            data_dic[w4] = w2


# 过滤当月时间
class FilterDataExcelPipeLine(object):

    def __init__(self):
        pass

# 讲数据统计到文档中

# 統計一篇文章記錄用戶的統計次數
article_count_times = {}


class WriteCleanDataAndCountTimes(object):

    def __init__(self):
        print '\n'+'WriteCleanDataAndCountTimes 正在初始化...'
        for k, v in data_dic.items():
            article_count_times[v] = 0

# 記錄規則，一篇文章一人多次回復視為一次
    def process_item(self, item, spider):
        if isinstance(item, HeimaKbdlDetailItem):
            # 判断是否是要统计的用户
            topsticks = item['topsticks']
            print '*' * 50
            u_list = []
            for topstick in topsticks[1:]:
                # 获取论坛名字
                username_bbs = topstick['username']
                if data_dic.has_key(username_bbs):
                    username = data_dic[username_bbs]
                    if username in u_list:
                        continue
                    u_list.append(username)
                    print u'检查到有  '+username +u' 回复了当前文章'
                    # 只要發現這篇文章中有記錄用戶評論，那麼久終止 並且自動+ 1
                    article_count_times[
                        username] = article_count_times[username] + 1
            print '*' * 50
        return item

    def spider_closed(self, spider):
        print '\n\n'
        print u'统计信息'+ str(article_count_times)
        print '\n\n'

# 将干净的数据写到xlsx中


class WriteCleanDataExcelPipeline(object):

    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        th_line = ['板块', '姓名', '论坛账号', '发布时间', '序号', '文章名称', '链接', '回复/查看']
        self.ws.append(th_line)

    def process_item(self, item, spider):
        if isinstance(item, HeimaKbdlItem):
            bankuai_name = item['name']
            username_bbs = item['author']
            username = u''
            if data_dic.has_key(username_bbs):
                username = data_dic[username_bbs]
            # update_time = item['topsticks'][0].get('replyTime')
            update_time = item['updateTime']
            title = item['title']
            copy_url = item['href']
            reply_info = item['replyNum'] + "/" + item['sawNum']
            line = [bankuai_name, username, username_bbs, update_time,
                    '', title, copy_url, reply_info]  # 把数据中每一项整理出来
            self.ws.append(line)  # 将数据以行的形式添加到xlsx中
            today = datetime.date.today()
            self.wb.save('heima-bankuai-list-' +
                         str(today) + '.xlsx')  # 保存xlsx文件
        return item
