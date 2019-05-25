# -*- coding: utf-8 -*-
import scrapy
import time
import execjs
from news_spider.items import NewsSpiderItem


class NewsSpider(scrapy.Spider):
    name = 'zhidx_bk'
    allowed_domains = ['zhidx.com']
    start_urls = ['http://zhidx.com']
    today = time.strftime('%m-%d', time.localtime())

    # today = '05-20'

    def parse(self, response):
        news_list = response.xpath("//ul[@class='info-list']/li")
        # first_page_oldest = news_list[len(news_list)-1].xpath("(.//div[@class='info-left-content']/div[@class='info-left-related']/div[@class='ilr-time'])[last()]/text()").extract_first().strip()
        # print('first_page_oldest:',first_page_oldest)
        # if first_page_oldest == self.today:
        #     execjs.eval("document.querySelector('.info-left-other').click()")
        # else:
        #     news_list = response.xpath("//ul[@class='info-list']/li")
        for info_item in news_list:
            news_item = NewsSpiderItem()
            news_item['published_at'] = info_item.xpath(".//div[@class='info-left-content']/div[@class='info-left-related']/div[@class='ilr-time']/text()").extract_first().strip()
            if self.today != news_item['published_at']:
                return
            else:
                news_item['title'] = info_item.xpath(".//div[@class='info-left-content']/div[@class='info-left-title']/a/text()").extract_first()
                news_item['origin_website'] = '智东西'
                news_item['origin_host'] = self.allowed_domains[0]
                news_item['origin_url'] = info_item.xpath(".//div[@class='info-left-content']/div[@class='info-left-title']/a/@href").extract_first()
                news_item['section'] = ''
                news_item['abstract'] = info_item.xpath(".//div[@class='info-left-content']/div[@class='info-left-desc']/text()").extract_first().strip()
                yield scrapy.Request(news_item['origin_url'], meta={'item': news_item}, callback=self.detail_parse)

    def detail_parse(self, response):
        item = response.meta['item']
        item['published_at'] = response.xpath("//div[@class='post-related']/span[@class='time']/text()").extract_first().strip().replace('/', '-')
        yield item
