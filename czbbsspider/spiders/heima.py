# -*- coding: utf-8 -*-
import scrapy
from czbbsspider.items import HeimaKbdlItem, HeimaKbdlDetailItem, HeimaKbdlDetailPassenerItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import re
import czbbsspider.utils as utils

import os
if __name__ == "__main__":
    print 'starting--------------------------------'
    # spider = HeimaSpider()
    # spider.start_requests()
    os.system('scrapy crawl heima')
    raw_input()



class HeimaSpider(CrawlSpider):
    name = "heima"
    base_url = 'http://bbs.itheima.com'
    domain_names = [
        u'开班典礼',
        u'班级活动',
        u'就业薪资',
        u'学员感言'
    ]
    rules = (
        Rule(LinkExtractor(allow=('&page=[0-9]+', ))),
    )

    start_urls = [
        # 'http://bbs.itheima.com/forum.php?mod=forumdisplay&fid=237&filter=typeid&typeid=627',
        'http://bbs.itheima.com/forum.php?mod=forumdisplay&fid=411&filter=typeid&typeid=686',
        'http://bbs.itheima.com/forum.php?mod=forumdisplay&fid=235&filter=typeid&typeid=605',
        'http://bbs.itheima.com/forum.php?mod=forumdisplay&fid=236&filter=typeid&typeid=647',
        'http://bbs.itheima.com/forum.php?mod=forumdisplay&fid=237&filter=typeid&typeid=632',
    ]
    
    def start(self):
        utils.print_tips_info()
        inp = raw_input('please input your choice:')
        return inp

    def start_requests(self):
        inp = self.start()
        if inp:
            self._input = inp
            for start_url in self.start_urls:
                yield Request(start_url, meta={'url': start_url}, callback=self.parse)

    def parse(self, response):
        self.domain_index = self.parse_domain_index(response.meta)
        if not self.domain_index:
            self.domain_index = 0
        # 查询共有几页数据
        total_page = response.xpath("//label/span/text()").extract_first()
        current_page = response.xpath(
            "//input[@name='custompage']/@value").extract_first()
        pages_full_url = self.start_urls[self.domain_index]
        if current_page:
            pages_full_url = pages_full_url + "&page=" + current_page
        yield Request(pages_full_url, meta={'current_page': current_page, "name": self.domain_names[self.domain_index]}, callback=self.parse_pages)

        pages = []
        page_total = 1
        if total_page:
            pages = re.findall("\d+", total_page)
        if pages and len(pages) > 0:
            page_total = pages[0]
        # int(page_total):
        if current_page and int(current_page) < int(page_total):
            print u" 11111当前第 %d 页  共%d页" % (int(current_page), int(page_total))
            next_page = int(current_page) + 1
            next_page_url = self.start_urls[
                self.domain_index] + "&page=" + str(next_page)
            yield Request(next_page_url, meta={"url": next_page_url}, callback=self.parse)

    def parse_domain_index(self, meta):
        if meta.has_key('url'):
            url = meta['url']
            if '686' in url:
                return 0
            elif '705' in url:
                return 1
            elif '647' in url:
                return 2
            elif '632' in url:
                return 3
        return 0

    def parse_pages(self, response):
        table = response.xpath("//table")
        current_page = response.meta['current_page']
        name = response.meta['name']
        print u"当前 %s 页面中共有 %s 条数据" % (current_page, len(table.xpath("tbody")))
        bankuai_levels = response.xpath(
            "//div[@class='bm cl']/div[@class='z']")
        bankuai_level = ''
        if not bankuai_level:
            for level in bankuai_levels.xpath('a'):
                bankuai_level = bankuai_level + "<<" + \
                    level.xpath('text()').extract_first()
        for tbody in table.xpath("tbody"):
            # print tbody.extract()
            title = tbody.xpath("tr/th/a/text()").extract_first()
            href = tbody.xpath("tr/th/a[@class='s xst']/@href").extract_first()
            if href:
                href = self.base_url +"/"+ href
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
            item = HeimaKbdlItem(
                bankuai_name    = bankuai_level,
                name            = name,
                title           = title,
                author          = author,
                updateTime      = updateTime,
                sawNum          = sawNum,
                replyNum        = replyNum,
                lastReplyAuthor = lastReplyAuthor,
                lastReplyTime   = lastReplyTime,
                href            = href)
            if self._input is '1' or self._input is '3':
                yield item
            if self._input is '2' or self._input is '3':
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
        bankuai_level = item['name']
        if not bankuai_level:
            for level in bankuai_levels.xpath('a'):
                bankuai_level = bankuai_level + "<<" + \
                    level.xpath('text()').extract_first()
        table = response.xpath("//table[@class='comiis_viewtop']")
        title = table.xpath("tr/td/h1/span/text()").extract_first()
        copy_url = self.base_url + '/' + \
            table.xpath("tr/td/span/a/@href").extract_first()
        passeners = []
        print '>>>>>>>>>>>' + bankuai_level + "<<" + item['title'] + u"中有" + item['replyNum'] + u"人回复"
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
            bankuai_name=bankuai_level, title=title, copy_url=copy_url, topsticks=passeners,
            replyNum=item['replyNum'],
            sawNum=item['sawNum'],
            updateTime=item['updateTime']
            )
        yield item
