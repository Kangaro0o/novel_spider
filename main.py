# !/usr/bin/python
# -*- coding: UTF-8 -*-

from db.mongodb import MongoDB
from utils.novel import Novel
from novel.zhuishu_spider import ZhuiShuSpider
from novel.babadushu_spider import BaBaDuShuSpider
from novel.liewen_spider import LieWenSpider


# zhuishu = ZhuiShuSpider()
# babadushu = BaBaDuShuSpider()
liewen = LieWenSpider()
mongodb = MongoDB('liewen')
novel = Novel(liewen, mongodb)
novel.fuzzy_search('好想')