# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
from news_spider.items import NewsSpiderItem
from news_spider.pipelines import NewsSpiderPipeline


class NewsSpider(scrapy.Spider):
    name = 'semi_ac'
    allowed_domains = ['www.semi.ac.cn']
    start_urls = ['http://www.semi.ac.cn/xwdt/kyjz/', 'http://www.semi.ac.cn/2017xshd_136831/', 'http://www.semi.ac.cn/xslw/']
    news_pipeline = NewsSpiderPipeline()
    db_cursor = news_pipeline.cursor
    db_cursor.execute("""select max(published_at) from news_source where origin_host = %s""", allowed_domains[0])
    deadline = int(db_cursor.fetchone()[0])

    def err_callback(self, response):
        print('----出错了----')
        print(response)

    def parse(self, response):
        news_list = response.xpath("//div[@class='ArticleList']/table/tbody/tr")
        news_list.pop()  # 去除最后一个空行
        relative_path = response.url.split('index')[0]
        for info_item in news_list:
            news_item = NewsSpiderItem()
            news_item['title'] = info_item.xpath(".//td[@class='fw_t']/a/text()").extract_first().strip()
            news_item['origin_website'] = '中国科学院半导体研究所'
            news_item['origin_host'] = self.allowed_domains[0]
            news_item['origin_url'] = relative_path + info_item.xpath(".//td[@class='fw_t']/a/@href").extract_first()[2:]
            news_item['section'] = response.xpath("string(//div[@class='Position'])").extract_first()
            news_item['abstract'] = ''
            news_item['created_at'] = int(datetime.datetime.now().timestamp())
            published_at = info_item.xpath(".//td[@class='fw_s']/text()").extract_first()
            if published_at:
                news_item['published_at'] = int(datetime.datetime.strptime('20' + published_at.strip(), "%Y-%m-%d").timestamp())
                if self.deadline > news_item['published_at']:
                    return
                yield news_item
            else:
                continue

        next_link = response.xpath("//div[@class='t_page ColorLink']/a[contains(text(),'下一页')]/@href").extract_first()

        if next_link:
            yield scrapy.Request(relative_path + next_link, callback=self.parse, errback=self.err_callback)
