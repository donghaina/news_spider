# -*- coding: utf-8 -*-
import scrapy
import time
from news_spider.items import NewsSpiderItem


class NewsSpider(scrapy.Spider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    def parse(self, response):
        news_list = response.xpath("//ul[@class='note-list']/li")
        for info_item in news_list:
            news_item = NewsSpiderItem()
            news_item['title'] = info_item.xpath(".//div[@class='content']/a[@class='title']/text()").extract_first()
            news_item['origin_url'] = info_item.xpath(".//div[@class='content']/a[@class='title']/@href").extract_first()
            news_item['abstract'] = info_item.xpath(".//div[@class='content']/p[@class='abstract']/text()").extract_first().strip()
            fo = open("result.txt", "a+", newline='')
            fo.write(news_item['title'] + '——' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n')
            # 关闭打开的文件
            fo.close()
            # print(news_item)
