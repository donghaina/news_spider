# -*- coding: utf-8 -*-
import scrapy
import time
from news_spider.items import NewsSpiderItem


class NewsSpider(scrapy.Spider):
    name = 'ai_ofweek'
    allowed_domains = ['ai.ofweek.com']
    start_urls = ['https://ai.ofweek.com/CAT-201718-nlp.html']
    # today = time.strftime('%Y-%m-%d', time.localtime())

    def parse(self, response):
        news_list = response.xpath("//div[contains(@class,'main-cont-left')]/div[@class='content']/div[contains(@class,'item-box')]")
        print(news_list)
        for info_item in news_list:
            news_item = NewsSpiderItem()
            info_item_content = info_item.xpath(".//div[contains(@class,'item-box-right')]")
            if info_item_content:
                info_item = info_item_content
            news_item['title'] = info_item.xpath(".//div[contains(@class,'top-title')]/a/text()").extract_first()
            news_item['origin_website'] = 'OFweek人工智能网'
            news_item['origin_host'] = self.allowed_domains[0]
            news_item['origin_url'] = info_item.xpath(".//div[contains(@class,'top-title')]/a/@href").extract_first()
            news_item['section'] = 'OFweek人工智能网 > 自然语言处理'
            news_item['abstract'] = ''
            text_bottom = info_item.xpath(".//div[contains(@class,'box-right-text')]")
            if text_bottom:
                news_item['published_at'] = info_item.xpath(".//div[@class='box-right-text-left']/span[5]/text()").extract_first().strip()[:10]
            else:
                news_item['published_at'] = info_item.xpath(".//div[contains(@class,'text-bottom')]//span[5]/text()").extract_first().strip()[:10]
            # if self.today != news_item['published_at']:
            #     return

            # print(news_item)
            yield news_item

