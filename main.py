# !/usr/bin/python
# -*- coding: UTF-8 -*-
from db.mongodb import MongoDB
from convert.convert_to_epub import ConvertToEpub
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

# cursor = mongodb.find(title='聊斋假太子')
# book = cursor.next()
# print(book)

# with open('./convert/epub2_templates/OPS/package.opf', encoding='utf-8', mode='r') as file:
#     content = file.read()
#     print(content.format(title='狄仁杰', author='安娜方法', publisher='盗亦有道'))

epub = ConvertToEpub("测试书")
# opf生成
opf = epub.set_opf(title='书名', author='作者', description='小说描述信息', date='2019-7-1', subject='灵异类',
                   items='<item></item>', itemsref='<itemref></itemref>')
print(opf)
