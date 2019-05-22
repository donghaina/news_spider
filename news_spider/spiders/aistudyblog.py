# -*- coding: utf-8 -*-
import scrapy
import time
from news_spider.items import NewsSpiderItem
import sys


class NewsSpider(scrapy.Spider):
    name = 'aistudyblog'
    allowed_domains = ['www.aistudyblog.com']
    start_urls = ['http://www.aistudyblog.com/']
    end = False
    # today = time.mktime(time.strptime('2019-05-01', '%Y-%m-%d'))

    today = time.time()
    
    def parse(self, response):
        nav_list = response.xpath("//div[@class='ns_area list']/ul/li[not(@class='first')]")
        section = {}
        for nav_item in nav_list:
            section['url'] = nav_item.xpath('./a/@href').extract_first()
            section['title'] = nav_item.xpath('./a/text()').extract_first()
            yield scrapy.Request('http://www.aistudyblog.com/' + section['url'], meta={'section': section}, callback=self.section_parse)

    def section_parse(self, response):
        news_item = NewsSpiderItem()
        news_list_1 = response.xpath("//div[@id='ndi_main']/div[contains(@class,'news_article')]/div[contains(@class,'na_detail')]")
        news_list_2 = response.xpath("//div[@id='ndi_main']/div[contains(@class,'news_special')]")
        for info_item in news_list_1:

            published_at_array = info_item.xpath(".//div[@class='news_tag']/span[@class='time']/text()").extract_first().strip().split('/')
            # print(published_at_array)
            published_at = published_at_array[0].zfill(2) + '-' + published_at_array[1].zfill(2) + '-' + published_at_array[2].split(' ')[0].zfill(2)
            # print(published_at)
            published_at_time = time.mktime(time.strptime(published_at, '%Y-%m-%d'))
            if (self.today - 24 * 60 * 60) >= published_at_time:
                return
            else:
                news_item['title'] = info_item.xpath(".//div[@class='news_title']/h3/a/text()").extract_first()
                news_item['origin_website'] = '人工智能科技'
                news_item['published_at'] = published_at
                news_item['origin_host'] = self.allowed_domains[0]
                news_item['origin_url'] = 'http://www.aistudyblog.com' + info_item.xpath(".//div[@class='news_title']/h3/a/@href").extract_first()
                news_item['section'] = '人工智能科技' + ' > ' + response.meta['section']['title']
                news_item['abstract'] = ''
                # print(news_item)
                yield news_item

        for info_item_2 in news_list_2:
            if end:
                return
            else:
                news_item['title'] = info_item_2.xpath(".//div[@class='news_title']/h3/strong/a/text()").extract_first()
                news_item['origin_website'] = '人工智能科技'
                news_item['origin_host'] = self.allowed_domains[0]
                news_item['origin_url'] = 'http://www.aistudyblog.com' + info_item_2.xpath(".//div[@class='news_title']/h3/strong/a/@href").extract_first()
                news_item['section'] = '人工智能科技' + ' > ' + response.meta['section']['title']
                news_item['abstract'] = ''
                yield scrapy.Request('http://www.aistudyblog.com/' + news_item['origin_url'], meta={'item': news_item}, callback=self.detail_parse)
            # yield news_item

    def detail_parse(self, response):
        item = response.meta['item']
        item['published_at'] = response.xpath("//div[@class='post_time_source']/text()").extract_first().strip()
        published_at_time = time.mktime(time.strptime(item['published_at'], '%Y-%m-%d'))
        if (self.today - 24 * 60 * 60) >= published_at_time:
            self.end = True
        else:
            yield (item)
