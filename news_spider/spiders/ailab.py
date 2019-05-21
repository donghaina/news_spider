# -*- coding: utf-8 -*-
import scrapy
import time
from news_spider.items import NewsSpiderItem


class ChinasmartgridSpider(scrapy.Spider):
    name = 'ailab'
    allowed_domains = ['www.ailab.cn']
    start_urls = ['http://www.ailab.cn']
    today = time.strftime('%Y-%m-%d', time.localtime())

    def parse(self, response):
        news_list = response.xpath("//ul[@class='list_jc']/li")

        for info_item in news_list:
            news_item = NewsSpiderItem()
            news_item['title'] = info_item.xpath(".//a[1]/@title").extract_first()
            news_item['origin_website'] = '人工智能实验室'
            news_item['origin_host'] = self.allowed_domains[0]
            news_item['origin_url'] = info_item.xpath(".//a[1]/@href").extract_first()
            news_item['section'] = '首页 > 热点信息'
            news_item['abstract'] = info_item.xpath(".//p[@class='cn']/text()").extract_first()
            news_item['published_at'] = info_item.xpath(".//p[@class='xx']/span[@class='rq']/text()").extract_first().strip()

            if self.today != news_item['published_at']:
                return

            yield news_item

        next_link = response.xpath(
            "//div[@class='col-left box mt10']/div[@class='pg']/a[@class='nxt']/@href").extract_first()

        if next_link:
            yield scrapy.Request('http://www.ailab.cn' + next_link, callback=self.parse)
