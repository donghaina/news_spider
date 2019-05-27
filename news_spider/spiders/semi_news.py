# -*- coding: utf-8 -*-
import scrapy
import datetime
from news_spider.items import NewsSpiderItem
from news_spider.pipelines import NewsSpiderPipeline


class NewsSpider(scrapy.Spider):
    name = 'semi_news'
    domain = 'http://www.semi.org.cn'
    allowed_domains = ['www.semi.org.cn']
    start_urls = ['http://www.semi.org.cn/news/news_list3.aspx']
    start_page = 0
    param_viewstate = ''
    param_viewstategenerator = ''
    news_pipeline = NewsSpiderPipeline()
    db_cursor = news_pipeline.cursor
    db_cursor.execute("""select max(published_at) from news_source where origin_host = %s""", allowed_domains[0])
    deadline = int(db_cursor.fetchone()[0])

    def parse_login(self, response):
        print('start to process login ')
        self.param_viewstate = response.xpath("//input[@name='__VIEWSTATE']/@value").extract_first()
        self.param_viewstategenerator = response.xpath("//input[@name='__VIEWSTATEGENERATOR']/@value").extract_first()
        print('start real request')
        return [
            scrapy.FormRequest(
                url=self.start_urls[0],
                formdata={'__EVENTTARGET': 'AspNetPager1',
                          '__EVENTARGUMENT': str(self.start_page),
                          '__VIEWSTATE': self.param_viewstate,
                          '__VIEWSTATEGENERATOR': self.param_viewstategenerator},
                callback=self.parse
            )
        ]

    def start_requests(self):
        return [scrapy.FormRequest(url=self.start_urls[0], formdata={}, callback=self.parse_login)]

    def parse(self, response):
        news_list = response.xpath("//table[@class='gongzuo']/tr")

        for info_item in news_list:
            news_item = NewsSpiderItem()
            news_item['title'] = info_item.xpath(".//td[1]//div[@class='jishu01']/a//span[@class='hei1']").extract_first().strip()
            news_item['origin_website'] = 'SEMI大导体产业网'
            news_item['origin_host'] = self.allowed_domains[0]
            news_item['origin_url'] = info_item.xpath(".//td[1]//div[@class='jishu01']/a/@href").extract_first().replace('..', self.domain)
            news_item['section'] = 'SEMI大导体产业网 > 热点新闻'
            news_item['abstract'] = info_item.xpath(".//td[1]//div[@class='jishu01']/a/text()").extract_first().strip()
            news_item['created_at'] = int(datetime.datetime.now().timestamp())
            yield scrapy.Request(news_item['origin_url'], meta={'item': news_item}, callback=self.detail_parse)

        next_link = response.xpath("//table[@id='AspNetPager1']//tr/td/a[contains('下一页',text())]/@href").extract_first()

        if next_link:
            self.start_page = self.start_page + 1
            print('正在爬第几页', self.start_page)
            yield scrapy.FormRequest(
                url=self.start_urls[0],
                formdata={'__EVENTTARGET': 'AspNetPager1',
                          '__EVENTARGUMENT': str(self.start_page),
                          '__VIEWSTATE': self.param_viewstate,
                          '__VIEWSTATEGENERATOR': self.param_viewstategenerator},
                callback=self.parse
            )

    def detail_parse(self, response):
        item = response.meta['item']
        published_at = response.xpath("//span[@id='lblTime']/text()").extract_first().strip()
        item['published_at'] = int(datetime.datetime.strptime(published_at, "%Y-%m-%d").timestamp())
        yield item
