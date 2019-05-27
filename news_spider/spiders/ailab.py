# -*- coding: utf-8 -*-
import scrapy
import time
import datetime
from news_spider.items import NewsSpiderItem
from news_spider.pipelines import NewsSpiderPipeline


class NewsSpider(scrapy.Spider):
    name = 'ailab'
    allowed_domains = ['www.ailab.cn']
    start_urls = ['http://www.ailab.cn']
    news_pipeline = NewsSpiderPipeline()
    db_cursor = news_pipeline.cursor
    db_cursor.execute("""select max(published_at) from news_source where origin_host = %s""", allowed_domains[0])
    deadline = int(db_cursor.fetchone()[0])

    def start_requests(self):
        return [scrapy.FormRequest(url=self.start_urls[0], dont_filter=True, callback=self.parse)]

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
            news_item['created_at'] = int(datetime.datetime.now().timestamp())
            published_at = info_item.xpath(".//p[@class='xx']/span[@class='rq']/text()").extract_first().strip()
            news_item['published_at'] = int(datetime.datetime.strptime(published_at, "%Y-%m-%d").timestamp())
            print(self.deadline, news_item['published_at'])
            if self.deadline > news_item['published_at']:
                return
            yield news_item

        next_link = response.xpath(
            "//div[@class='col-left box mt10']/div[@class='pg']/a[@class='nxt']/@href").extract_first()
        if next_link:
            yield scrapy.Request(next_link, callback=self.parse)
