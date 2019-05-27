# -*- coding: utf-8 -*-
import scrapy
import datetime
from news_spider.items import NewsSpiderItem
from news_spider.pipelines import NewsSpiderPipeline


class NewsSpider(scrapy.Spider):
    name = 'chinasmartgrid'
    allowed_domains = ['www.chinasmartgrid.com.cn']
    start_urls = ['http://www.chinasmartgrid.com.cn/List-News?rid=119']
    news_pipeline = NewsSpiderPipeline()
    db_cursor = news_pipeline.cursor
    db_cursor.execute("""select max(published_at) from news_source where origin_host = %s""", allowed_domains[0])
    deadline = int(db_cursor.fetchone()[0])

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
            news_item['created_at'] = int(datetime.datetime.now().timestamp())
            published_at = info_item.xpath(".//span/text()").extract_first().strip()
            news_item['published_at'] = int(datetime.datetime.strptime(published_at, "%Y-%m-%d").timestamp())
            if self.deadline >= news_item['published_at']:
                return
            yield news_item

        next_link = response.xpath("//div[@class='list_page']/div[@class='page']/a[@title='下一页']/@href").extract_first()

        if next_link:
            yield scrapy.Request('http://www.chinasmartgrid.com.cn/' + next_link, callback=self.parse)
