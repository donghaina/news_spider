# -*- coding: utf-8 -*-
import scrapy
import time
from news_spider.items import NewsSpiderItem


class NewsSpider(scrapy.Spider):
    name = 'elecfans'
    allowed_domains = ['www.elecfans.com']
    start_urls = ['http://www.elecfans.com/rengongzhineng']
    # today = time.strftime('%m-%d', time.localtime())
    # today = '2019-03-26'
    # today = time.mktime(time.strptime('2019-03-25', '%Y-%m-%d'))
    today = time.time()

    def parse(self, response):
        news_list = response.xpath("//div[@class='article-list']")
        for info_item in news_list:
            news_item = NewsSpiderItem()
            published_at = info_item.xpath(".//div[@class='a-content']/p[@class='one-more clearfix']/span[@class='time']/text()").extract_first().strip()
            published_at_time = time.mktime(time.strptime(published_at, '%Y-%m-%d'))
            if (self.today-24*60*60) >= published_at_time:
                return
            else:
                news_item['published_at'] = published_at
                news_item['title'] = info_item.xpath(".//div[@class='a-content']/h3[@class='a-title']/a/text()").extract_first()
                news_item['origin_website'] = '电子发烧友网'
                news_item['origin_host'] = self.allowed_domains[0]
                news_item['origin_url'] = info_item.xpath(".//div[@class='a-content']/h3[@class='a-title']/a/@href").extract_first()
                news_item['section'] = '电子发烧友网 > 人工智能'
                news_item['abstract'] = info_item.xpath(".//div[@class='a-content']/p[@class='a-summary']/text()").extract_first().strip()
                yield news_item
                # print(news_item)

        next_link = response.xpath(
            "//div[@class='pagn1']/a[@class='page-next']/@href").extract_first()

        if next_link:
            yield scrapy.Request('http://www.elecfans.com/rengongzhineng/' + next_link, callback=self.parse)
