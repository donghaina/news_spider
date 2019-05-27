# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
from news_spider.items import NewsSpiderItem
from news_spider.pipelines import NewsSpiderPipeline

class NewsSpider(scrapy.Spider):
    name = 'zhidx'
    allowed_domains = ['zhidx.com']
    start_urls = ['http://zhidx.com/wp-admin/admin-ajax.php']
    start_page = 1
    news_pipeline = NewsSpiderPipeline()
    db_cursor = news_pipeline.cursor
    db_cursor.execute("""select max(published_at) from news_source where origin_host = %s""", allowed_domains[0])
    deadline = int(db_cursor.fetchone()[0])
    def start_requests(self):
        return [scrapy.FormRequest(url=self.start_urls[0], formdata={'action': 'category_list', 'page': str(self.start_page)}, callback=self.parse_list)]

    def parse_list(self, response):
        news_item = NewsSpiderItem()
        news_list = json.loads(response.body_as_unicode())['result']
        if len(news_list) == 0:
            return
        else:
            for info_item in news_list:
                news_item['title'] = info_item['title']
                news_item['origin_website'] = '智东西'
                news_item['created_at'] = int(datetime.datetime.now().timestamp())
                news_item['origin_host'] = self.allowed_domains[0]
                news_item['origin_url'] = info_item['link']
                news_item['section'] = ''
                news_item['abstract'] = info_item['desp']
                yield scrapy.Request(news_item['origin_url'], meta={'item': news_item}, callback=self.detail_parse)

            self.start_page = self.start_page + 1
            yield scrapy.FormRequest(
                url=self.start_urls[0],
                formdata={'action': 'category_list', 'page': str(self.start_page)},
                callback=self.parse_list
            )

    def detail_parse(self, response):
        item = response.meta['item']
        published_at = response.xpath("//div[@class='post-related']/span[@class='time']/text()").extract_first().strip()
        item['published_at'] = int(datetime.datetime.strptime(published_at, "%Y/%m/%d").timestamp())
        yield item
