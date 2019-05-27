# -*- coding: utf-8 -*-
import scrapy
import datetime
from news_spider.items import NewsSpiderItem
from news_spider.pipelines import NewsSpiderPipeline

class NewsSpider(scrapy.Spider):
    name = 'elecfans'
    allowed_domains = ['www.elecfans.com']
    start_urls = ['http://www.elecfans.com/rengongzhineng']
    news_pipeline = NewsSpiderPipeline()
    db_cursor = news_pipeline.cursor
    db_cursor.execute("""select max(published_at) from news_source where origin_host = %s""", allowed_domains[0])
    deadline = int(db_cursor.fetchone()[0])
    def parse(self, response):
        news_list = response.xpath("//div[@class='article-list']")
        for info_item in news_list:
            news_item = NewsSpiderItem()
            published_at = info_item.xpath(".//div[@class='a-content']/p[@class='one-more clearfix']/span[@class='time']/text()").extract_first().strip()
            news_item['title'] = info_item.xpath(".//div[@class='a-content']/h3[@class='a-title']/a/text()").extract_first()
            news_item['origin_website'] = '电子发烧友网'
            news_item['origin_host'] = self.allowed_domains[0]
            news_item['origin_url'] = info_item.xpath(".//div[@class='a-content']/h3[@class='a-title']/a/@href").extract_first()
            news_item['section'] = '电子发烧友网 > 人工智能'
            news_item['created_at'] = int(datetime.datetime.now().timestamp())
            news_item['published_at'] = int(datetime.datetime.strptime(published_at, "%Y-%m-%d").timestamp())
            news_item['abstract'] = info_item.xpath(".//div[@class='a-content']/p[@class='a-summary']/text()").extract_first().strip()
            yield news_item

        next_link = response.xpath("//div[@class='pagn1']/a[@class='page-next']/@href").extract_first()

        if next_link:
            yield scrapy.Request('http://www.elecfans.com/rengongzhineng/' + next_link, callback=self.parse)
