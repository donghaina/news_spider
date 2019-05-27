# -*- coding: utf-8 -*-
import datetime
import scrapy
import time
import datetime
from news_spider.items import NewsSpiderItem
from news_spider.pipelines import NewsSpiderPipeline


# 状态，完成了后续页面的抓取，第一个页面的需要单独添加
class NewsSpider(scrapy.Spider):
    name = 'semi_car'
    domain = 'http://ecar.semi.org.cn/'
    allowed_domains = ['ecar.semi.org.cn']
    start_page = 1
    start_urls = ['http://ecar.semi.org.cn']
    news_pipeline = NewsSpiderPipeline()
    db_cursor = news_pipeline.cursor
    db_cursor.execute("""select max(published_at) from news_source where origin_host = %s""", allowed_domains[0])
    deadline = int(db_cursor.fetchone()[0])

    # parse first page
    def parse(self, response):
        news_list = response.xpath("//div[@class='list']")

        for info_item in news_list:
            news_item = NewsSpiderItem()
            news_item['title'] = info_item.xpath(".//h2/a/text()").extract_first()
            news_item['origin_website'] = 'SEMI大导体产业网'
            news_item['origin_host'] = self.allowed_domains[0]
            news_item['origin_url'] = info_item.xpath(".//h2/a/@href").extract_first()
            news_item['section'] = 'SEMI大导体产业网 > 汽车电子应用'
            news_item['abstract'] = info_item.xpath(".//div[@class='abstract']/text()").extract_first().strip()
            news_item['created_at'] = int(datetime.datetime.now().timestamp())
            published_at = info_item.xpath(".//div[@class='inputdate']/text()").extract_first()
            news_item['published_at'] = self.parse_timestamp(published_at)
            if self.deadline >= news_item['published_at']:
                return
            yield news_item

        self.start_page = self.start_page + 1
        yield scrapy.Request('http://ecar.semi.org.cn/indexLoading_' + str(self.start_page) + '.html', callback=self.parse)

    def parse_timestamp(self, dataStr):
        ts = 0
        dateStr = (str(dataStr)).split('\xa0\xa0')
        if (len(dateStr) > 1):
            dateNow = dateStr[1].strip()
            dt = datetime.datetime.strptime(dateNow, "%Y-%m-%d %H:%M:%S")
            ts = dt.timestamp()
        return int(ts)
