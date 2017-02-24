import os
if __name__ == "__main__":
    print 'starting--------------------------------'
    # spider = HeimaSpider()
    # spider.start_requests()
    os.system('scrapy crawl heima')
    raw_input()