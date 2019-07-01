# !/usr/bin/python
# -*- coding: UTF-8 -*-
from convert.converter import Converter
from config.settings import EPUB_DIR, EPUB_SOURCE, EPUB_RIGHTS, EPUB_PUBLISHER, EPUB_BUILDER, EPUB_PROVIDER
import os
from datetime import date
from uuid import uuid4
from utils.in_memory_zip import InMemoryZip


class ConvertToEpub(Converter):
    """生成 epub 电子书"""

    # epub 模板路径
    templates_path = './convert/epub2_templates/'

    def __init__(self, title, author, cover, intro, chapters):
        # 如果目录不存在，则创建一个
        if not os.path.isdir(EPUB_DIR):
            os.mkdir(EPUB_DIR)
        # 文件保存位置
        self.__dir = EPUB_DIR
        # 书籍固定信息
        self.__publisher = EPUB_PUBLISHER
        self.__source = EPUB_SOURCE
        self.__rights = EPUB_RIGHTS
        self.__builder = EPUB_BUILDER
        self.__provider = EPUB_PROVIDER
        # 书籍动态信息
        self.__title = title
        self.__author = author
        self.__cover = cover
        self.__intro = intro
        self.__chapters = chapters
        # 模板文件句柄
        self.__mimetype = open(self.templates_path + 'mimetype',
                               encoding='utf-8', mode='r')
        self.__container = open(self.templates_path + 'META-INF/container.xml',
                                encoding='utf-8', mode='r')
        self.__opf = open(self.templates_path + 'OPS/package.opf',
                          encoding='utf-8', mode='r')
        self.__cover = open(self.templates_path + 'OPS/coverpage.html',
                            encoding='utf-8', mode='r')
        self.__ncx = open(self.templates_path + 'OPS/TOC.ncx',
                          encoding='utf-8', mode='r')
        self.__chapter = open(self.templates_path + 'OPS/chapter_template.html',
                              encoding='utf-8', mode='r')

    def __del__(self):
        self.__mimetype.close()
        self.__container.close()
        self.__opf.close()
        self.__cover.close()
        self.__ncx.close()
        self.__chapter.close()

    def set_mimetype(self):
        return self.__mimetype.read()

    def set_container(self):
        return self.__container.read()

    def set_cover(self):
        """小说封面"""
        content = self.__cover.read()
        return content.format(publisher=self.__publisher, builder=self.__builder,
                              rights=self.__rights, title=self.__title, author=self.__author, intro=self.__intro)

    def set_ncx(self):
        # 生成 navPoint
        nav_points = []
        for i, chapter in enumerate(self.__chapters):
            nav_points.append('''
<navPoint id="chapter{id}" playOrder="1">
<navLabel><text>{title}</text></navLabel>
<content src="chapter{id}.html"/>
</navPoint>'''.format(id=(i+1), title=chapter['title']))
        nav_points = '\n'.join(nav_points)
        content = self.__ncx.read()
        uuid = uuid4()
        return content.format(uuid4=uuid, provider=self.__provider, builder=self.__builder,
                              rights=self.__rights, title=self.__title, author=self.__author, nav_points=nav_points)

    def set_chapter(self, chapter_title, chapter_content):
        """生成章节内容"""
        content = self.__chapter.read()
        return content.format(provider=self.__provider, builder=self.__builder, rights=self.__rights,
                              title=chapter_title, content=chapter_content)

    def set_opf(self, subject=None):
        """
        生成 package.opf
        利用 chapters(title,url,content)
        """
        length = len(self.__chapters)
        items = []
        itemsref = []
        # 生成 items itemsref
        for i in range(1, length + 1):
            items.append(
                '<item id="chapter{id}"  href="chapter{id}.html"  media-type="application/xhtml+xml"/>'.format(id=i))
            itemsref.append(
                '<itemref idref="chapter{id}" linear="yes"/>'.format(id=i))
        items = "\n".join(items)
        itemsref = "\n".join(itemsref)
        content = self.__opf.read()
        today = date.today()
        return content.format(publisher=self.__publisher, source=self.__source, rights=self.__rights, date=today, subject=subject,
                              items=items, itemsref=itemsref, title=self.__title, author=self.__author, description=self.__intro)

    def make(self, title, author, intro, chapters):
        pass
        # self.__make_info(title, author, intro)
        # for chapter in chapters:
        #     self.__make_chapter(chapter['title'], chapter['content'])
