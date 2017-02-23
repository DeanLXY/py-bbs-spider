# -*- coding: utf-8 -*-
import scrapy
from czbbsspider.items import HeimaKbdlItem, HeimaKbdlDetailItem, HeimaKbdlDetailPassenerItem
from scrapy.http import Request
import re

class HeimaSpider(scrapy.Spider):
    name = "heima"
    base_url = 'http://bbs.itheima.com'
    domain_names = [
        u'开班典礼',
        u'班级活动',
        u'就业薪资',
        u'学员感言'
    ]
    start_urls = [
        'http://bbs.itheima.com/forum.php?mod=forumdisplay&fid=237&filter=typeid&typeid=627',
        'http://bbs.itheima.com/forum.php?mod=forumdisplay&fid=411&filter=typeid&typeid=686',
        'http://bbs.itheima.com/forum.php?mod=forumdisplay&fid=235&filter=typeid&typeid=605',
        'http://bbs.itheima.com/forum.php?mod=forumdisplay&fid=236&filter=typeid&typeid=647',
        'http://bbs.itheima.com/forum.php?mod=forumdisplay&fid=237&filter=typeid&typeid=632'
    ]

    # domain_index = 0

    def parse(self, response):
        print "_____________________________________________________"
        table = response.xpath("//table")
        # 查询共有几页数据
        total_page = response.xpath("//label/span/text()").extract()
        pages = []
        page_total = 1
        if total_page:
            pages = re.findall("\d+", total_page[0])
        if pages and len(pages)>0:
            page_total = pages[0]
        if page_total != 1:
            next_page_url = 
            yield Request(next_page_url, callback=self.parse)
        for tbody in table.xpath("tbody"):
            # print tbody.extract()
            title = tbody.xpath("tr/th/a/text()").extract_first()
            href = tbody.xpath("tr/th/a/@href").extract()
            author = tbody.xpath(
                "tr/td[@class='by']/cite/a/text()").extract_first()
            updateTime = tbody.xpath(
                "tr/td[@class='by']/em/span/text()").extract_first()
            if not updateTime:
                updateTime = tbody.xpath(
                    "tr/td[@class='by']/em/span/span/text()").extract_first()
            replyNum = tbody.xpath(
                "tr/td[@class='num']/a/text()").extract_first()
            sawNum = tbody.xpath(
                "tr/td[@class='num']/em/text()").extract_first()
            lastReplyAuthor = tbody.xpath(
                "tr/td[@class='by']/cite/a/text()").extract()
            lastReplyTime = tbody.xpath(
                "tr/td[@class='by']/em/a/text()").extract_first()
            if not lastReplyTime:
                lastReplyTime = tbody.xpath(
                    "tr/td[@class='by']/em/a/span/text()").extract_first()
            item = HeimaKbdlItem(title=title, author=author, updateTime=updateTime, sawNum=sawNum,
                                 replyNum=replyNum, lastReplyAuthor=lastReplyAuthor, lastReplyTime=lastReplyTime, href=href)
            # yield item
            if href:
                full_url = ''
                if len(href) == 1:
                    full_url = self.base_url + "/" + href[0]
                else:
                    full_url = self.base_url + "/" + href[1]
                yield Request(full_url, meta={'item': item}, callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta['item']
        bankuai_levels = response.xpath(
            "//div[@class='bm cl']/div[@class='z']")
        bankuai_level = ''
        for level in bankuai_levels.xpath('a'):
            bankuai_level = bankuai_level + "<<" + \
                level.xpath('text()').extract_first()
        table = response.xpath("//table[@class='comiis_viewtop']")
        title = table.xpath("tr/td/h1/span/text()").extract_first()
        copy_url = self.base_url + '/' + \
            table.xpath("tr/td/span/a/@href").extract_first()
        passeners = []
        print '\n\n'
        print "<<" + bankuai_level + u"中有" + item['replyNum'] + u"人回复"
        for table_plhin in response.xpath("//table[@class='plhin']"):
            # print '--------------'
            reply_author = table_plhin.xpath(
                "tr/td/div/div/div/a/text()").extract_first()
            reply_time_dump = table_plhin.xpath("tr/td/div/div/div/*")
            for time in reply_time_dump:
                if time.xpath("@id").re(r'authorposton(\d+)'):
                    reply_time = time.xpath("text()").extract_first()
            reply_content = table_plhin.xpath(
                "tr/td/div/div/div/table/tr/td/text()").extract_first()
            # print "%s##%s##%s" %(reply_author, reply_time, reply_content)
            passenerItem = HeimaKbdlDetailPassenerItem(
                username=reply_author, replyTime=reply_time, replyContent=reply_content)
            # print passenerItem
            passeners.append(dict(passenerItem))
        item = HeimaKbdlDetailItem(
            bankuai_name=bankuai_level, title=title, copy_url=copy_url, topsticks=passeners)
        yield item
