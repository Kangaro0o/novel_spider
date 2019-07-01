# !/usr/bin/python
# -*- coding: UTF-8 -*-

from db.mongodb import MongoDB
# from utils.spider import Spider
# from novel.zhuishu_spider import ZhuiShuSpider
# from novel.babadushu_spider import BaBaDuShuSpider
# from novel.liewen_spider import LieWenSpider
# from convert.convert_to_txt import ConvertToTxt
# from utils.generator import Generator
# zhuishu = ZhuiShuSpider()
# babadushu = BaBaDuShuSpider()
# liewen = LieWenSpider()
mongodb = MongoDB('liewen')
# novel = Spider(zhuishu, mongodb)
# novel.fuzzy_search('将夜')

# cursor = mongodb.find(title='死神列车', author='死神钓者')
# for book in cursor:
#     converter = ConvertToTxt(book['title'])
#     g = Generator(converter)
#     g.make(book)

cursor = mongodb.find(title='聊斋假太子')
book = cursor.next()
