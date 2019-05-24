# -*- coding: utf-8 -*-
import datetime
import scrapy
import time
import datetime
from news_spider.items import NewsSpiderItem


#状态，完成了后续页面的抓取，第一个页面的需要单独添加
class ChinasmartgridSpider(scrapy.Spider):
    name = 'semi_car'
    domain = 'http://ecar.semi.org.cn/'
    allowed_domains = ['ecar.semi.org.cn']
    i = 2
    start_urls = ['http://ecar.semi.org.cn/indexLoading_2.html']
    deadline = int(time.time()) - 10 * 24 * 3600 #暂时只抓取10天之内的数据

    #parse first page
    def parse(self, response):
        news_list = response.xpath("//div[@class='list']")

        for info_item in news_list:
            news_item = NewsSpiderItem()
            news_item['title'] = info_item.xpath(".//h2/a/text()").extract_first()
            news_item['origin_website'] = 'SEMI大导体产业网'
            news_item['origin_host'] = self.allowed_domains[0]
            news_item['origin_url'] = info_item.xpath(".//h2/a/@href").extract_first()
            news_item['section'] = 'SEMI大导体产业网 > 汽车电子应用'
            news_item['abstract'] = info_item.xpath(".//div[@class='abstract']/text()").extract_first().strip()
            news_item['published_at'] = self.parseTimestamp(info_item.xpath(".//div[@class='inputdate']/text()").extract_first())
            print(news_item)


            if self.deadline > news_item['published_at']:
                return

            # print(news_item)

            yield news_item

        self.i = self.i + 1
        yield scrapy.Request('http://ecar.semi.org.cn/indexLoading_'+ str(self.i) +'.html', callback=self.parse)

    def parseTimestamp(self, dataStr):
        ts = 0
        print(dataStr)
        dateStr = (str(dataStr)).split('\xa0\xa0')
        print(dateStr)
        if(len(dateStr) > 1):
            dateNow = dateStr[1].strip()

            dt = datetime.datetime.strptime(dateNow, "%Y-%m-%d %H:%M:%S")
            ts = dt.timestamp()
        return int(ts)
