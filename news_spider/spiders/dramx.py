# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
from news_spider.items import NewsSpiderItem


class NewsSpider(scrapy.Spider):
    name = 'dramx'
    allowed_domains = ['www.dramx.com']
    start_urls = ['https://www.dramx.com/News/', 'https://www.dramx.com/Market/', 'https://www.dramx.com/Topic/']

    def err_callback(self, response):
        print('----出错了----')
        print(response)

    def parse(self, response):
        print(response.headers)
        news_list = response.xpath("//div[@id='divArticleList']/div[contains(@class,'Article-box-cont')]/div[@class='Article-content']")
        for info_item in news_list:
            news_item = NewsSpiderItem()
            news_item['title'] = info_item.xpath(".//h3/a/text()").extract_first().strip()
            news_item['origin_website'] = '全球半导体观察'
            news_item['origin_host'] = self.allowed_domains[0]
            news_item['origin_url'] = 'https://www.dramx.com' + info_item.xpath(".//h3/a/@href").extract_first()
            news_item['section'] = '全球半导体观察 > ' + response.xpath("//a[@class='Article-boxtitle-active']/text()").extract_first()
            news_item['abstract'] = info_item.xpath(".//p[@class='Article-essay']/text()").extract_first()
            news_item['created_at'] = int(datetime.datetime.now().timestamp())
            yield scrapy.Request(news_item['origin_url'], meta={'item': news_item}, callback=self.detail_parse)

        next_link = response.xpath("(//div[@class='jogger']/a)[last()]/@href").extract_first()

        if next_link:
            yield scrapy.Request('https://www.dramx.com' + next_link, callback=self.parse, errback=self.err_callback)

    def detail_parse(self, response):
        item = response.meta['item']
        published_at = response.xpath("//div[@class='newstitle-bottom']/p/time/text()").extract_first().strip()
        item['published_at'] = int(datetime.datetime.strptime(published_at, "%Y-%m-%d %H:%M:%S").timestamp())
        # print(item)
        yield item