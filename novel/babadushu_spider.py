# !/usr/bin/python
# -*- coding: UTF-8 -*-
from novel.novel_spider import NovelSpider
from config.sites import BABADUSHU, BABADUSHU_SEARCH, BABADUSHU_HEADERS
import requests
from requests.exceptions import ConnectionError, Timeout
from requests.adapters import HTTPAdapter
from config.settings import MAX_RETRIES
from pyquery import PyQuery as pq
from math import ceil


class BaBaDuShuSpider(NovelSpider):
    """
    88读书小说网爬虫实现
    """

    def __init__(self):
        super(BaBaDuShuSpider, self).__init__()
        self.__site_url = BABADUSHU  # 88读书网首页
        self.__search_url = BABADUSHU_SEARCH  # 88读书网搜素地址
        self.__headers = BABADUSHU_HEADERS  # 头信息
        self.__s = requests.Session()
        self.__s.mount('https://', HTTPAdapter(max_retries=MAX_RETRIES))
        self.__s.mount('http://', HTTPAdapter(max_retries=MAX_RETRIES))
        # 记录当前小说目录链接
        self.__chapters_url = ''

    def __del__(self):
        """释放请求资源"""
        self.__s.close()

    def get_search_html(self, keyword, page=1):
        """
        根据关键字搜索图书
        :param keyword: 搜索关键字
        :param page: 当前页码
        :return: 搜索返回的 源码
        """
        params = {
            'search_field': '0',
            'q': keyword,
            'page': page
        }
        try:
            response = self.__s.get(self.__search_url, params=params, headers=self.__headers)
            if response.status_code == 200:
                return response.text
            return None
        except ConnectionError as e:
            print("A Connection error occurred.",e.args)
        except Timeout as e:
            print("The request timed out.", e.args)

    def __get_search_pages(self, search_html):
        """计算出搜素结果的页数"""
        doc = pq(search_html)
        # 获取搜素结果总数
        search_result_total = doc.find('.ops_lf')
        total = int(search_result_total.find('em:last-child').text())
        per_page = 10
        max_page = ceil(total/per_page)
        return 1 if max_page == 0 else max_page

    def get_search_result(self, search_html):
        """传入搜素结果某一页的源码，然后解析"""
        doc = pq(search_html)
        selector = '.ops_cover .block_txt p:first-child'
        books = doc.find(selector)
        if books:
            for book in books.items():
                yield {
                    'title': book.find('h2').text(),
                    'chapters_url': book.find('a').attr('href')
                }

    def get_search_results(self, keyword):
        """查询结果，返回（书名和链接）列表"""
        page = 0
        max_page = 1
        results = []  # 存储搜素结果的图书链接
        while page < max_page:
            page += 1  # 当前页
            print('正在访问第', page, '页 ')
            search_html = self.get_search_html(keyword, page)  # 第 page 页的源码
            if search_html:
                max_page = self.__get_search_pages(search_html)  # 最大页数
                result = self.get_search_result(search_html)
                for r in result:
                    results.append({
                        'title': r['title'],
                        'chapters_url': r['chapters_url']
                    })
            else:
                print("第", page, "页无法访问")
        return results if len(results) > 0 else None

    def get_chapters_html(self, chapters_url):
        self.__chapters_url = chapters_url
        """获取小说目录页的源码"""
        try:
            response = self.__s.get(chapters_url, headers=self.__headers)
            if response.status_code == 200:
                return response.content.decode('gbk')
            return None
        except ConnectionError as e:
            print("A Connection error occurred.", e.args)
        except Timeout as e:
            print("The request timed out.", e.args)

    def get_novel_info(self, chapters_html):
        """获取小说基本信息（作者、简介等）"""
        doc = pq(chapters_html)
        main_info = doc.find('.jieshao')
        cover = main_info.find('.lf img').attr('src')
        title = main_info.find('.rt h1')  # 书名
        author = main_info.find('.rt .msg em:first-child')
        status = main_info.find('.rt .msg em:nth-child(2)')
        intro = main_info.find('.rt .intro')  # 简介
        info = {
            'cover': cover,
            'title': title.text(),
            'author': author.text()[3:],
            'status': status.text()[3:],
            'intro': intro.text()
        }
        return info

    def get_chapters(self, chapters_html):
        doc = pq(chapters_html)
        chapters = doc.find('.mulu ul li a')
        for chapter in chapters.items():
            yield {
                'title': chapter.text(),
                'url': self.__chapters_url + chapter.attr('href')
            }

    def get_chapter_html(self, chapter_url):
        try:
            response = self.__s.get(chapter_url, headers=self.__headers)
            if response.status_code == 200:
                return response.content
            return None
        except ConnectionError as e:
            print("A Connection error occurred.", e.args)
        except Timeout as e:
            print("The request timed out.", e.args)

    def get_chapter_content(self, chapter_html):
        doc = pq(chapter_html)
        content = doc.find('.novel .yd_text2')
        return content.text()
