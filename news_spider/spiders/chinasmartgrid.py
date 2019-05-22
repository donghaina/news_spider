# -*- coding: utf-8 -*-
import scrapy
import time
from news_spider.items import NewsSpiderItem


class NewsSpider(scrapy.Spider):
    name = 'chinasmartgrid'
    allowed_domains = ['www.chinasmartgrid.com.cn']
    start_urls = ['http://www.chinasmartgrid.com.cn/List-News?rid=119']
    today = time.strftime('%Y-%m-%d', time.localtime())

    def parse(self, response):
        news_list = response.xpath("//ul[@class='list_left_ul']/li[not(@class='dashed_line')]")

        for info_item in news_list:
            news_item = NewsSpiderItem()
            news_item['title'] = info_item.xpath(".//a/@title").extract_first()
            news_item['origin_website'] = '智能电网市场'
            news_item['origin_host'] = self.allowed_domains[0]
            news_item['origin_url'] = info_item.xpath(".//a/@href").extract_first()
            news_item['section'] = '北极星智能电网在线 > 市场'
            news_item['abstract'] = ''
            news_item['published_at'] = info_item.xpath(".//span/text()").extract_first().strip()

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
