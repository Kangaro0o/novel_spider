# !/usr/bin/python
# -*- coding: UTF-8 -*-

from novel.zhuishu_spider import ZhuiShuSpider
from db.mongodb import MongoDB
from utils.novel import Novel


zhuishu_spider = ZhuiShuSpider()
mongodb = MongoDB('zhuishu')
novel = Novel(zhuishu_spider, mongodb)

kw = '带着工业革命系统回明朝'
novel.search(kw)
