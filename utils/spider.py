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

    def __save(self, results):
        """存储小说内容，要确保 results 不为空"""
        for result in results:
            title = result['title']  # 小说名
            chapters_url = result['chapters_url']
            print('正在爬取', title)
            # 获取目录页源码
            chapters_html = self._spider.get_chapters_html(chapters_url)
            if chapters_html:  # 如果请求到了小说目录页
                # 获取小说基本信息
                book_info = self._spider.get_novel_info(chapters_html)
                # 先把小说基本信息添加到数据库
                _id = self._db.add(book_info)
                # 接着遍历小说章节内容
                chapters = self._spider.get_chapters(chapters_html)
                for chapter in chapters:
                    chapter_url = chapter['url']
                    chapter_title = chapter['title']
                    # 追加小说章节内容到数据库
                    print('正在访问', chapter_title, chapter_url)
                    chapter_html = self._spider.get_chapter_html(chapter_url)
                    if chapter_html:  # 如果获取到了章节内容源码
                        chapter_content = self._spider.get_chapter_content(chapter_html)
                        # 追加存储到数据库
                        self._db.append(ObjectId(_id), {
                            'chapters': {
                                'title': chapter_title,
                                'url': chapter_url,
                                'content': chapter_content
                            }
                        })
                        print(chapter_title, 'Saved Successfully')
                        time.sleep(1)
                    else:
                        print(chapter_title, chapter_url, "无法爬取")
                print(title, 'has already finished!')
                time.sleep(1)
            else:
                print(title, '无法爬取')
        print('ALL DONE!')

    def fuzzy_search(self, keyword):
        """模糊搜素小说，存储到数据库"""
        results = self._spider.get_search_results(keyword)
        if results:  # 如果查找到了相关小说
            self.__save(results)
        else:
            print("找不到和", keyword, '相关的小说')

    def search(self, keyword):
        """精确搜素"""
        results = self._spider.get_search_results(keyword)
        books = [] # 存储符合条件的书
        if results:
            for result in results:
                title = result['title']  # 小说名
                # 精确搜素，只有与关键字完全相同的小说才会被存储
                if title == keyword:
                    books.append(result)
            # 此时 books 里存储的就是我们需要的书
            if books:
                self.__save(books)
            else:
                print('未搜素到与', keyword, '同名的小说')
        else:
            print('找不到和', keyword, '相关的小说')
