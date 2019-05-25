# -*- coding: utf-8 -*-
import datetime
import scrapy
import time
import datetime
from news_spider.items import NewsSpiderItem


class NewsSpider(scrapy.Spider):
    name = 'semi_ic'
    domain = 'http://www.semi.org.cn/technology/'
    allowed_domains = ['www.semi.org.cn']
    start_urls = ['http://www.semi.org.cn/technology/news_list.aspx?classid=19']
    start_page = 0

    deadline = int(time.time()) - 10 * 24 * 3600  # 暂时只抓取10天之内的数据
    param_viewstate = ''
    param_viewstategenerator = ''

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
            published_at_text = info_item.xpath(".//td[2]/text()").extract_first().strip()
            news_item['title'] = info_item.xpath(".//td[@class='zuobian']/a/text()").extract_first()
            news_item['origin_website'] = 'SEMI大导体产业网'
            news_item['origin_host'] = self.allowed_domains[0]
            news_item['origin_url'] = self.domain + info_item.xpath(".//td[@class='zuobian']/a/@href").extract_first()
            news_item['section'] = '大导体产业网 > IC设计与制造'
            news_item['abstract'] = ''
            news_item['published_at'] = int(datetime.datetime.strptime(published_at_text, "%Y-%m-%d").timestamp())
            news_item['created_at'] = int(datetime.datetime.now().timestamp())
            yield news_item
        #     if self.deadline > news_item['published_at']:
        #         return
        #
        next_link = response.xpath("//table[@id='AspNetPager1']//tr/td/a[contains('下一页',text())]/@href").extract_first()

        if next_link:
            self.start_page = self.start_page + 1
            yield scrapy.FormRequest(
                url=self.start_urls[0],
                formdata={'__EVENTTARGET': 'AspNetPager1',
                          '__EVENTARGUMENT': str(self.start_page),
                          '__VIEWSTATE': self.param_viewstate,
                          '__VIEWSTATEGENERATOR': self.param_viewstategenerator},
                callback=self.parse
            )
