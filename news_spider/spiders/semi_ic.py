# -*- coding: utf-8 -*-
import datetime
import scrapy
import time
import datetime
from news_spider.items import NewsSpiderItem



class ChinasmartgridSpider(scrapy.Spider):
    name = 'semi_ic'
    domain = 'http://www.semi.org.cn/technology/'
    allowed_domains = ['www.semi.org.cn/']
    start_urls = ['http://www.semi.org.cn/technology/news_list.aspx?classid=19']
    start_page = 0

    deadline = int(time.time()) - 10 * 24 * 3600  # 暂时只抓取10天之内的数据
    param_viewstate = ''
    param_viewstategenerator = ''

    def login(self):
        print('start to login ')
        formdata = {}
        yield scrapy.FormRequest(url = self.start_urls[0], formdata=formdata, callback=self.parse_login)

    def parse_login(self, response):
        print('start to process login ')
        self.param_viewstate = response.xpath("//input[@name='__VIEWSTATE']/@value").extract_first()
        self.param_viewstategenerator = response.xpath("//input[$name='__VIEWSTATEGENERATOR']/@value").extract_first()
        yield super().start_requests()

    def request_pages(self, response):
        self.start_page = self.start_page + 1
        print('start real request')
        yield scrapy.FormRequest(
            url=self.start_urls[0],
            formdata={'__EVENTTARGET': 'AspNetPager1',
                      '__EVENTARGUMENT': str(self.start_page),
                      '__VIEWSTATE': self.param_viewstate,
                      '__VIEWSTATEGENERATOR': self.param_viewstategenerator},
            callback=self.parse
        )

    def parse(self, response):
        print(response.xpath("//div[@class='weizhi']/a/text()").extract_first())
        news_list = response.xpath("//table[@class='gongzuo']/tbody/tr")

        print(news_list)
        for info_item in news_list:
            news_item = NewsSpiderItem()
            news_item['title'] = info_item.xpath(".//td/a/text()").extract_first()
            news_item['origin_website'] = 'SEMI大导体产业网'
            news_item['origin_host'] = self.allowed_domains[0]
            news_item['origin_url'] = self.domain + info_item.xpath(".//td/a/@href").extract_first()
            news_item['section'] = 'SEMI大导体产业网 > IC设计与制造'
            news_item['published_at'] = self.parseTimestamp(info_item.xpath(".//td[last()]/text()").extract_first())


            print(news_item)

            if self.deadline > news_item['published_at']:
                return

            print(news_item)

            yield scrapy.Request(news_item['origin_url'], meta={'item': news_item}, callback=self.detail_parse)

            yield news_item

        next_link = response.xpath(
            "//div[@class='list_page']/div[@class='page']/a[@title='下一页']/@href").extract_first()

        if next_link:
            yield scrapy.Request('http://www.semi.org.cn/technology/news_list.aspx?classid=19', callback=self.parse)

            # yield news_item

    def detail_parse(self, response):
        item = response.meta['item']
        item['title'] = response.xpath("//td[@class='xinwenbiaoti']/span/text()").extract_first().strip()
        subItem = response.xpath("//td[@class='contenttext']/p/text()")
        print(subItem[0])
        item['abstract'] = subItem[0]

    def parseTimestamp(self, dataStr):
        dt = datetime.datetime.strptime(dataStr, "%Y-%m-%d")
        ts = dt.timestamp()
        return int(ts)
