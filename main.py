# !/usr/bin/python
# -*- coding: UTF-8 -*-
from utils.in_memory_zip import InMemoryZip
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


# opf生成
# cursor = mongodb.find(title='聊斋假太子')
# book = cursor.next()
# epub = ConvertToEpub(book['title'], book['author'],
#                      book['cover'], book['intro'], book['chapters'])

# opf = epub.set_opf()
# print(opf)


# 生成 mimetype
# mimetype = epub.set_mimetype()

# 生成container.xml
# container = epub.set_container()

# 生成 ncx
"""
<navPoint id="chapter15" playOrder="15">
<navLabel><text>尾声</text></navLabel>
<content src="chapter15.html"/>
"""
# ncx = epub.set_ncx(title='novel name', author='liuwen', nav_points='<biaiqoain:>')
# print(ncx)

# 生成封面
# cover = epub.set_cover(title='novel name', author='kelvin', intro='this is intro')
# print(cover)

# from uuid import uuid4
# print(uuid4())

if __name__ == '__main__':
    cursor = mongodb.find(title='聊斋假太子')
    book = cursor.next()
    epub = ConvertToEpub(book['title'], book['author'],
                         book['cover'], book['intro'], book['chapters'])
    # cover = epub.set_cover()
    # print(cover)
    # cnx = epub.set_ncx()
    # print(cnx)

    title = book['chapters'][0]['title']
    content = book['chapters'][0]['content']

    chapter = epub.set_chapter(title, content)
    print(chapter)
