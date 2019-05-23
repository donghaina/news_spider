# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    origin_website = scrapy.Field()
    origin_host = scrapy.Field()
    origin_url = scrapy.Field()
    abstract = scrapy.Field()
    section = scrapy.Field()
    published_at = scrapy.Field()
    created_at = scrapy.Field()
