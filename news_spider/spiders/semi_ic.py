# -*- coding: utf-8 -*-
import datetime
import scrapy
import time
import datetime
from news_spider.items import NewsSpiderItem



class ChinasmartgridSpider(scrapy.Spider):
    name = 'semi_car'
    domain = 'http://www.semi.org.cn/technology/'
    allowed_domains = ['http://www.semi.org.cn/']
    start_urls = ['http://www.semi.org.cn/technology/news_list.aspx?classid=19']
    today = time.strftime('%Y-%m-%d', time.localtime())

    #parse first page
    def parse(self, response):
        news_list = response.xpath("//table[@class='gongzuo']")

        for info_item in news_list:
            news_item = NewsSpiderItem()
            news_item['title'] = info_item.xpath(".//td/a/text()").extract_first()
            news_item['origin_website'] = 'SEMI大导体产业网'
            news_item['origin_host'] = self.allowed_domains[0]
            news_item['origin_url'] = self.domain + info_item.xpath(".//td/a/@href").extract_first()
            news_item['section'] = 'SEMI大导体产业网 > IC设计与制造'
            news_item['abstract'] = ''
            news_item['published_at'] = self.parseTimestamp(info_item.xpath(".//td[last()]/text()"))

            if self.today != news_item['published_at']:
                return

            # print(news_item)

            yield news_item
        # for info_item in news_list:
        #     yield {
        #         'title': info_item.xpath(".//a/@title").extract_first(),
        #         'origin_website': '智能电网市场',
        #         'origin_host': self.allowed_domains[0],
        #         'origin_url': info_item.xpath(".//a/@href").extract_first(),
        #         'published_at': info_item.xpath(".//span/text()").extract_first()
        #     }

        next_link = response.xpath("//div[@class='list_page']/div[@class='page']/a[@title='下一页']/@href").extract_first()

        if next_link:
            yield scrapy.Request('http://www.chinasmartgrid.com.cn/' + next_link, callback=self.parse)

    def parseTimestamp(self, dataStr):
        dateStr = dataStr.split('&nbsp;&nbsp;')
        dateNow = dateStr[1].strip()
        print(dateNow)

        dt = datetime.datetime.strptime(dateNow, "%Y-%m-%d")
        ts = dt.timestamp()
        return int(ts)
