# !/usr/bin/python
# -*- coding: UTF-8 -*-
from db.mongodb import MongoDB
from convert.convert_to_txt import ConvertToTxt
from convert.convert_to_epub import ConvertToEpub
from common import spider, generator
from novel.zhuishu_spider import ZhuiShuSpider
from novel.babadushu_spider import BaBaDuShuSpider
from novel.liewen_spider import LieWenSpider


def download_all(title=None):

    if title is not None:
        zhuishu = ZhuiShuSpider()
        # babadushu = BaBaDuShuSpider()
        # liewen = LieWenSpider()
        mongodb = MongoDB('zhuishu')
        # 想要爬取哪个网站，就把哪个网站的爬虫实现类传入，比如，我这里传入的是 追书网实例
        novel = spider.Spider(zhuishu, mongodb)
        novel.fuzzy_search(title)
    else:
        print('请输入要下载的小说名')


def download(title=None):
    if title is not None:
        zhuishu = ZhuiShuSpider()
        # babadushu = BaBaDuShuSpider()
        # liewen = LieWenSpider()
        mongodb = MongoDB('zhuishu')
        # 想要爬取哪个网站，就把哪个网站的爬虫实现类传入，比如，我这里传入的是 追书网实例
        novel = spider.Spider(zhuishu, mongodb)
        novel.search(title)
    else:
        print('请输入要下载的小说名')


def make_txt(book):
    converter = ConvertToTxt(book['title'])
    g = generator.Generator(converter)
    g.make(book)


def make_epub(book):
    epub = ConvertToEpub(book['title'], book['author'], book['cover'], book['intro'], book['chapters'])
    epub.make()


if __name__ == '__main__':
    mongodb = MongoDB('zhuishu')
    book = mongodb.find(title='天将夜').next()
    make_epub(book)
