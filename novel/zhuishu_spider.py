# !/usr/bin/python
# -*- coding: UTF-8 -*-

from common.novel_spider import NovelSpider
from urllib.parse import urlencode
from config.urls import ZhuiShu_Index, ZhuiShu_Search, ZhuiShu_Headers
import requests
from pyquery import PyQuery as pq


class ZhuiShuSpider(NovelSpider):
    """
    追书网小说爬虫实现
    """
    def __init__(self):
        super(ZhuiShuSpider, self).__init__()
        self._site_url = ZhuiShu_Index
        self._search_url = ZhuiShu_Search
        self._headers = ZhuiShu_Headers

    def search_page(self, keyword):
        params = {
            'keyword': keyword
        }
        url = self._search_url + urlencode(params)
        try:
            response = requests.get(url, headers=self._headers)
            if response.status_code == 200:
                return response.text
            return None
        except requests.ConnectionError:
            print('Failed to request', url)
            pass

    def parse_search_page(self, search_html):
        doc = pq(search_html)
        selector = 'div.result-game-item-detail > h3 > a'
        results = doc.find(selector)
        if results:
            for result in results.items():
                yield {
                    'title': result.text(),
                    'chapters_url': result.attr('href')
                }
        else:
            print('找不到')

    def get_chapters_page(self, chapters_url):
        try:
            response = requests.get(chapters_url, headers=self._headers)
            if response.status_code == 200:
                return response.content.decode('utf-8')
            return None
        except requests.ConnectionError:
            print('Failed to request', chapters_url)
            pass

    def parse_novel_info(self, chapters_html):
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

    def parse_chapters_page(self, chapters_html):
        doc = pq(chapters_html)
        chapters = doc.find('.box_con > #list > dl > dd > a')
        for chapter in chapters.items():
            yield {
                'title': chapter.text(),
                'url': self._site_url + chapter.attr('href')
            }

    def get_chapter_page(self, chapter_url):
        try:
            response = requests.get(chapter_url, headers=self._headers)
            if response.status_code == 200:
                return response.content.decode('utf-8')
            return None
        except requests.ConnectionError:
            print('Failed to request', chapter_url)
            pass

    def parse_chapter_page(self, chapter_html):
        doc = pq(chapter_html)
        content = doc.find('#content')
        return content.text()