# !/usr/bin/python
# -*- coding: UTF-8 -*-


class NovelSpider:
    """
    定义小说爬虫的父类方法
    """

    def __init__(self):
        """
        初始化一些参数
        """
        pass

    def get_search_html(self, keyword, page=1):
        """
        根据关键字搜索图书
        :param keyword: 搜索关键字
        :param page: 当前页码
        :return: 搜索返回的 源码
        """
        pass

    def get_search_results(self, search_html):
        """
        解析搜索页
        :param search_html: 搜索后的源码
        :return: 搜索结果列表
        """
        pass

    def get_chapters_html(self, chapters_url):
        """
        请求具体某本小说的目录页
        :param chapters_url:
        :return: 目录页源码
        """
        pass

    def get_novel_info(self, chapters_html):
        """
        解析小说目录页 获取小说基本信息(小说名、作者、简介等)
        :param chapters_html:
        :return: 小说基本信息
        """
        pass

    def get_chapters(self, chapters_html):
        """
        解析目录页源码 获取小说目录
        :param chapters_html:
        :return: 小说目录
        """
        pass

    def get_chapter_html(self, chapter_url):
        """
        获取小说单章 HTML
        :param chapter_url:
        :return: 某一章节的源码
        """
        pass

    def get_chapter_content(self, chapter_html):
        """
        解析某一章节的源码
        :param chapter_html:
        :return: 章节内容
        """
        pass
