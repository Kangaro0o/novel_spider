# !/usr/bin/python
# -*- coding: UTF-8 -*-
from bson.objectid import ObjectId
import time

class Novel:
    """
    集成多个小说站点爬虫
    """

    def __init__(self, novel_spider, database):
        self._spider = novel_spider
        self._db = database

    def search(self, keyword):
        # 搜索关键字
        search_page = self._spider.search_page(keyword)
        # 解析搜索结果
        results = self._spider.parse_search_page(search_page)
        for result in results:
            print('正在爬', result['title'])
            # 获取目录页源码
            chapters_html = self._spider.get_chapters_page(result['chapters_url'])
            # 获取小说基本信息
            book_info = self._spider.parse_novel_info(chapters_html)
            # 把小说基本信息添加到数据库
            _id = self._db.add(book_info)
            book_chapters = self._spider.parse_chapters_page(chapters_html)
            for chapter in book_chapters:
                print('正在爬取', chapter['title'], chapter['url'])
                chapter_html = self._spider.get_chapter_page(chapter['url'])
                content = self._spider.parse_chapter_page(chapter_html)
                self._db.append(ObjectId(_id), {
                    'chapters': {
                        'title': chapter['title'],
                        'url': chapter['url'],
                        'content': content
                    },
                })
                print(chapter['title'], 'Saved Successfully')
                time.sleep(1)
            print(result['title'], 'finished!')
        print('done!')
