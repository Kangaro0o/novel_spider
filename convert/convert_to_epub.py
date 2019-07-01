# !/usr/bin/python
# -*- coding: UTF-8 -*-
from convert.converter import Converter
from config.settings import EPUB_DIR, EPUB_SOURCE, EPUB_RIGHTS, EPUB_PUBLISHER
import os


class ConvertToEpub(Converter):
    """生成 epub 电子书"""

    def __init__(self, filename):
        # 如果目录不存在，则创建一个
        if not os.path.isdir(EPUB_DIR):
            os.mkdir(EPUB_DIR)
        self.__dir = EPUB_DIR
        self.__opf = open('./convert/epub2_templates/OPS/package.opf',
                          encoding='utf-8', mode='r')

    def __del__(self):
        self.__opf.close()

    def set_opf(self, **kwargs):
        """
        kwargs:
         - title: 书名
         - author: 作者
         - publisher: 出版社
         - description: 描述
         - source: 来源
         - date: 日期
         - rights: 版权
         - subject: 主题
        """
        content = self.__opf.read()
        return content.format(publisher=EPUB_PUBLISHER, source=EPUB_SOURCE, rights=EPUB_RIGHTS, **kwargs)

    def make(self, title, author, intro, chapters):
        pass
        # self.__make_info(title, author, intro)
        # for chapter in chapters:
        #     self.__make_chapter(chapter['title'], chapter['content'])
