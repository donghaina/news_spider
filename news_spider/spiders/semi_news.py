# -*- coding: utf-8 -*-
import scrapy
import time
from news_spider.items import NewsSpiderItem


class ChinasmartgridSpider(scrapy.Spider):
    name = 'semi_news'
    domain = 'http://www.semi.org.cn'
    allowed_domains = ['http://www.semi.org.cn']
    start_urls = ['http://www.semi.org.cn/news/news_list3.aspx']
    today = time.strftime('%Y-%m-%d', time.localtime())

    def parse(self, response):
        news_list = response.xpath("//div[@class='jishu01']/a")

        for info_item in news_list:
            news_item = NewsSpiderItem()
            news_item['title'] = info_item.xpath("./strong").extract_first()
            news_item['origin_website'] = 'SEMI大导体产业网'
            news_item['origin_host'] = self.allowed_domains[0]
            news_item['origin_url'] = info_item.xpath(".//a/strong").extract_first().replace('..', self.domain)
            news_item['section'] = 'SEMI大导体产业网 > 热点新闻'
            news_item['abstract'] = info_item.xpath("./text()")
            news_item['published_at'] = '' #在列表页面找不到发布的时间，需要

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
