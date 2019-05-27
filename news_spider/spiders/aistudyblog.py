# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
from news_spider.items import NewsSpiderItem
from news_spider.pipelines import NewsSpiderPipeline


class NewsSpider(scrapy.Spider):
    name = 'aistudyblog'
    allowed_domains = ['www.aistudyblog.com']
    start_urls = ['http://www.aistudyblog.com/handler/CMSList.ashx?ActionType=InformationAllTypeList&InformationPage=1']
    start_page = 1
    news_pipeline = NewsSpiderPipeline()
    db_cursor = news_pipeline.cursor
    db_cursor.execute("""select max(published_at) from news_source where origin_host = %s""", allowed_domains[0])
    deadline = int(db_cursor.fetchone()[0])

    def parse(self, response):
        news_item = NewsSpiderItem()
        news_list = json.loads(response.body_as_unicode())['info']['list']
        if len(news_list) == 0:
            return
        else:
            for info_item in news_list:
                news_item['title'] = info_item['Title']
                news_item['origin_website'] = '人工智能科技'
                news_item['created_at'] = int(datetime.datetime.now().timestamp())
                news_item['published_at'] = int(datetime.datetime.strptime(info_item['CreateTime'], "%Y-%m-%d").timestamp())
                if self.deadline >= news_item['published_at']:
                    return
                news_item['origin_host'] = self.allowed_domains[0]
                news_item['origin_url'] = 'http://www.aistudyblog.com' + info_item['Url']
                news_item['section'] = '人工智能科技' + ' > ' + info_item['TypeName']
                news_item['abstract'] = info_item['Description']
                yield news_item

            self.start_page = self.start_page + 1
            next_link = 'http://www.aistudyblog.com/handler/CMSList.ashx?ActionType=InformationAllTypeList&InformationPage=' + str(self.start_page)
            yield scrapy.Request(next_link, callback=self.parse)
