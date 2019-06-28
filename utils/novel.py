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

    def fuzzy_search(self, keyword):
        """模糊搜素小说，存储到数据库"""
        results = self._spider.get_search_results(keyword)
        if results:  # 如果查找到了相关小说
            for result in results:
                title = result['title']  # 小说名
                print('正在爬取', title)
                chapters_url = result['chapters_url']
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
                        else:
                            print(chapter_title, chapter_url, "无法爬取")
                    print(title, 'has already finished!')
                else:
                    print(title, '无法爬取')
            print('ALL DONE!')
        else:
            print("找不到和", keyword, '相关的小说')

