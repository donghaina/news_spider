# -*- coding: utf-8 -*-


BOT_NAME = 'news_spider'

SPIDER_MODULES = ['news_spider.spiders']
NEWSPIDER_MODULE = 'news_spider.spiders'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 3

ITEM_PIPELINES = {
    'news_spider.pipelines.NewsSpiderPipeline': 3
}

MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'news'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
