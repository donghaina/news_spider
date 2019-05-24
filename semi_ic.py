import requests
import urllib.request
from bs4 import BeautifulSoup
import os
import time
import datetime
import pymysql
import execjs

db_connect = pymysql.connect(
    host='localhost',
    port=3306,
    db='news',
    user='root',
    passwd='root',
    charset='utf8',
    use_unicode=True)

# 通过cursor执行增删查改
cursor = db_connect.cursor()

start_url = 'http://www.semi.org.cn/technology/news_list.aspx?classid=19'
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(start_url, headers=headers)  # 使用headers避免访问受限
soup = BeautifulSoup(response.content, 'html.parser')
items = soup.select('.gongzuo tr')
__VIEWSTATE= soup.find('input',name='__VIEWSTATE')('value')
print(__VIEWSTATE)
# for item in items:
#     published_at_text = item.select('td')[1].get_text().strip()
#     news = {
#         'title': item.select('.zuobian')[0].get_text().strip(),
#         'origin_website': '大半导体产业网',
#         'origin_host': 'http://www.semi.org.cn',
#         'origin_url': 'http://www.semi.org.cn/technology/' + item.select('.zuobian a')[0]['href'].strip(),
#         'section': '首页 > IC设计与制造',
#         'abstract': '',
#         'created_at': int(datetime.datetime.now().timestamp()),
#         'published_at': int(datetime.datetime.strptime(published_at_text, "%Y-%m-%d").timestamp())
#     }
#
#     try:
#         # 查重处理
#         cursor.execute(
#             """select * from source where title = %s""",
#             news['title'])
#         # 是否有重复数据
#         repetition = cursor.fetchone()
#
#         # 重复
#         if repetition:
#             pass
#
#         else:
#             # 插入数据
#             instert_sql = """insert into source(title, origin_website,origin_url, origin_host, abstract, section, published_at,created_at) values ('%s','%s', '%s', '%s', '%s', '%s', '%s',%s)""" % (
#                 news['title'], news['origin_website'], news['origin_url'], news['origin_host'], news['abstract'], news['section'], news['published_at'], news['created_at'])
#
#             cursor.execute(instert_sql)
#
#             # 提交sql语句
#         db_connect.commit()
#
#     except Exception as error:
#         # 出现错误时打印错误日志
#         print('——————————出错误了——————————————', error)


next_link = soup.find('a',text='下一页')
# print(next_link)
# if next_link:
#     execjs.eval("document.getElementById('AspNetPager1').querySelectorAll('a')[5].click()")
