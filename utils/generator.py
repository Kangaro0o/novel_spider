# !/usr/bin/python
# -*- coding: UTF-8 -*-


class Generator:
    """
    生成各种格式的小说
    """

    def __init__(self, converter):
        self.__converter = converter

    def make(self, book_info):
        self.__converter.make(book_info['title'], book_info['author'],
                              book_info['intro'], book_info['chapters'])
        print(book_info['title'] + '。txt', '已合成')