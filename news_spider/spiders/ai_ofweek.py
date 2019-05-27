# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
from news_spider.items import NewsSpiderItem
from news_spider.pipelines import NewsSpiderPipeline


class NewsSpider(scrapy.Spider):
    name = 'ai_ofweek'
    allowed_domains = ['ai.ofweek.com']
    start_urls = ['https://ai.ofweek.com/CAT-201718-nlp-1.html']
    start_page = 1
    news_pipeline = NewsSpiderPipeline()
    db_cursor = news_pipeline.cursor
    db_cursor.execute("""select max(published_at) from news_source where origin_host = %s""", allowed_domains[0])
    deadline = int(db_cursor.fetchone()[0])

    def parse(self, response):
        news_list = json.loads(response.body_as_unicode())['newsList']
        for info_item in news_list:
            news_item = NewsSpiderItem()
            news_item['title'] = info_item['title']
            news_item['origin_website'] = 'OFweek人工智能网'
            news_item['origin_host'] = self.allowed_domains[0]
            news_item['origin_url'] = info_item['htmlpath']
            news_item['section'] = 'OFweek人工智能网 > 自然语言处理'
            news_item['abstract'] = info_item['summery']
            news_item['created_at'] = int(datetime.datetime.now().timestamp())
            news_item['published_at'] = int(datetime.datetime.strptime(info_item['addtimeStr'], "%Y-%m-%d %H:%M:%S").timestamp())

            if self.deadline >= news_item['published_at']:
                return

            yield news_item
        self.start_page = self.start_page + 1
        next_link = 'https://ai.ofweek.com/CAT-201718-nlp-' + str(self.start_page) + '.html'
        yield scrapy.Request(next_link, callback=self.parse)
