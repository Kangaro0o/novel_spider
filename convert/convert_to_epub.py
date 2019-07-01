# !/usr/bin/python
# -*- coding: UTF-8 -*-
from convert.converter import Converter
from config.settings import EPUB_DIR
import os

class ConvertToEpub(Converter):
    """生成 epub 电子书"""

    def __init__(self, filename):
        # 如果目录不存在，则创建一个
        if not os.path.isdir(EPUB_DIR):
            os.mkdir(EPUB_DIR)
        self.__dir = EPUB_DIR
        # self.__filename = self.__dir + filename + '.txt'

    def make(self, title, author, intro, chapters):
        pass
        # self.__make_info(title, author, intro)
        # for chapter in chapters:
        #     self.__make_chapter(chapter['title'], chapter['content'])