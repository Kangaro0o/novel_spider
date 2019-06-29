# !/usr/bin/python
# -*- coding: UTF-8 -*-

from novel.zhuishu_spider import ZhuiShuSpider
from db.mongodb import MongoDB
from utils.novel import Novel
from novel.babadushu_spider import BaBaDuShuSpider


# zhuishu_spider = ZhuiShuSpider()
babadushu = BaBaDuShuSpider()
mongodb = MongoDB('babadushu')
novel = Novel(babadushu, mongodb)
novel.search('琴帝')