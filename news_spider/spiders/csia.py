# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
from news_spider.items import NewsSpiderItem
from news_spider.pipelines import NewsSpiderPipeline


class NewsSpider(scrapy.Spider):
    name = 'csia'
    allowed_domains = ['www.csia.net.cn']
    start_urls = ['http://www.csia.net.cn/Article/ShowClass.asp?ClassID=80&page=1']
    news_pipeline = NewsSpiderPipeline()
    db_cursor = news_pipeline.cursor
    db_cursor.execute("""select max(published_at) from news_source where origin_host = %s""", allowed_domains[0])
    deadline = int(db_cursor.fetchone()[0])

    def err_callback(self, response):
        print('----出错了----')
        print(response)

    def parse(self, response):
        news_list = response.xpath("//td[@id='ArticleBody']/ul/li")
        for info_item in news_list:
            news_item = NewsSpiderItem()
            news_item['title'] = info_item.xpath(".//p/a/span/text()").extract_first()
            news_item['origin_website'] = '中国半导体行业协会'
            news_item['origin_host'] = self.allowed_domains[0]
            news_item['origin_url'] = info_item.xpath(".//p/a/@href").extract_first()
            news_item['section'] = '中国半导体行业协会 > 行业要闻'
            news_item['abstract'] = ''
            news_item['created_at'] = int(datetime.datetime.now().timestamp())
            published_at_text = info_item.xpath(".//p/span[2]/text()").extract_first()
            if published_at_text:
                print(published_at_text)
                published_at = re.sub(u"[(\()(\))]", "", published_at_text.strip())
                news_item['published_at'] = int(datetime.datetime.strptime(published_at, "%Y-%m-%d %H:%M:%S").timestamp())
                if self.deadline >= news_item['published_at']:
                    return
            else:
                continue
            # print(news_item)
            yield news_item

        next_link = response.xpath(
            "//div[@class='showpage']/form/a[contains(text(),'下一页')]/@href").extract_first()

        if next_link:
            yield scrapy.Request('http://www.csia.net.cn/Article/' + next_link, callback=self.parse, errback=self.err_callback)
