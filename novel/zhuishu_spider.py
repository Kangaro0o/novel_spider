# !/usr/bin/python
# -*- coding: UTF-8 -*-

from novel.novel_spider import NovelSpider
from urllib.parse import urlparse, parse_qsl
from config.sites import ZHUISHU, ZHUISHU_SEARCH, ZHUISHU_HEADERS
import requests
from requests.exceptions import ConnectionError, Timeout
from requests.adapters import HTTPAdapter
from pyquery import PyQuery as pq
from config.settings import MAX_RETRIES


class ZhuiShuSpider(NovelSpider):
    """
    追书网小说爬虫实现
    """

    def __init__(self):
        super(ZhuiShuSpider, self).__init__()
        self.__site_url = ZHUISHU  # 追书网首页
        self.__search_url = ZHUISHU_SEARCH  # 追书网搜索URL
        self.__headers = ZHUISHU_HEADERS  # 头信息
        # 初始化请求对象
        self.__s = requests.Session()
        self.__s.mount('https://', HTTPAdapter(max_retries=MAX_RETRIES))
        self.__s.mount('http://', HTTPAdapter(max_retries=MAX_RETRIES))

    def __del__(self):
        self.__s.close()

    def get_search_html(self, keyword, page=1):
        """获取搜索页的源码"""
        params = {
            'keyword': keyword,
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
        max_page = '1'  # 默认最大页为1
        doc = pq(search_html)
        # 获取分页容器对象
        search_result_page = doc.find('.search-result-page-main')
        # 判断是否存在分页：子节点中存在a标签则认为有分页
        is_paginated = search_result_page.children().is_('a')
        if is_paginated:
            last_page_url = search_result_page.find(
                'a:last-child').attr('href')
            # url 解码
            last_url = urlparse(last_page_url)
            params = dict(parse_qsl(last_url.query))
            max_page = params['page']
        return max_page

    def get_search_result(self, search_html):
        """传入搜素结果某一页的源码，然后解析"""
        doc = pq(search_html)
        selector = 'div.result-game-item-detail > h3 > a'
        books = doc.find(selector)
        if books:
            for book in books.items():
                yield {
                    'title': book.text(),
                    'chapters_url': book.attr('href')
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
                max_page = int(self.__get_search_pages(search_html))  # 最大页数
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
        """获取小说目录页的源码"""
        try:
            response = self.__s.get(chapters_url, headers=self.__headers)
            if response.status_code == 200:
                return response.content.decode('utf-8')
            return None
        except ConnectionError as e:
            print("A Connection error occurred.", e.args)
        except Timeout as e:
            print("The request timed out.", e.args)

    def get_novel_info(self, chapters_html):
        """获取小说基本信息（作者、简介等）"""
        doc = pq(chapters_html)
        main_info = doc.find('.box_con #maininfo')
        img = doc.find('#fmimg img')
        title = main_info.find('#info h1')  # 书名
        author = main_info.children('#info p').eq(0)
        status = main_info.children('#info p').eq(1).remove('a')
        intro = main_info.find('#intro')  # 简介
        cover = img.attr('src')
        info = {
            'cover': cover,
            'title': title.text(),
            'author': author.text()[7:],
            'status': status.text()[7:-3],
            'intro': intro.text()
        }
        return info

    def get_chapters(self, chapters_html):
        doc = pq(chapters_html)
        chapters = doc.find('.box_con > #list > dl > dd > a')
        for chapter in chapters.items():
            yield {
                'title': chapter.text(),
                'url': self.__site_url + chapter.attr('href')
            }

    def get_chapter_html(self, chapter_url):
        try:
            response = self.__s.get(chapter_url, headers=self.__headers)
            if response.status_code == 200:
                return response.content.decode('utf-8')
            return None
        except ConnectionError as e:
            print("A Connection error occurred.", e.args)
        except Timeout as e:
            print("The request timed out.", e.args)

    def get_chapter_content(self, chapter_html):
        doc = pq(chapter_html)
        content = doc.find('#content')
        return content.text()
