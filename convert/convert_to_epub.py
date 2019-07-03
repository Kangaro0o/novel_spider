# !/usr/bin/python
# -*- coding: UTF-8 -*-
from convert.converter import Converter
from config.settings import EPUB_DIR, EPUB_SOURCE, EPUB_RIGHTS, EPUB_PUBLISHER, EPUB_BUILDER, EPUB_PROVIDER
import os
from datetime import date
from uuid import uuid4
import requests
from requests.exceptions import ConnectionError, Timeout
import zipfile


class ConvertToEpub(Converter):
    """生成 epub 电子书"""

    # epub 模板路径
    _templates_path = './convert/epub2_templates'

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
        # 模板文件路径
        self.__container = self._templates_path + '/META-INF/container.xml'
        self.__opf = self._templates_path + '/OPS/fb.opf'
        self.__cover_page = self._templates_path + '/OPS/coverpage.html'
        self.__ncx = self._templates_path + '/OPS/fb.ncx'
        self.__chapter = self._templates_path + '/OPS/chapter_template.html'
        # zip 文件对象
        self.__epub = zipfile.ZipFile(self.__dir + self.__title+'.epub', 'a', compression=zipfile.ZIP_DEFLATED)

    def __del__(self):
        self.__epub.close()

    def write_mimetype(self):
        self.__epub.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        return self

    def write_container(self):
        with open(self.__container, 'r', encoding='utf-8') as f:
            self.__epub.writestr('META-INF/container.xml', f.read())
        return self

    def write_opf(self, subject=None):
        """
        生成 fb.opf
        """
        items = []
        itemrefs = []
        # 生成 items itemsref
        for i in range(1, len(self.__chapters) + 1):
            items.append('<item id="chapter{id}"  href="chapter{id}.html"  '
                         'media-type="application/xhtml+xml"/>'.format(id=i))
            itemrefs.append('<itemref idref="chapter{id}" linear="yes"/>'.format(id=i))
        items = "\n".join(items)
        itemrefs = "\n".join(itemrefs)

        today = date.today()
        with open(self.__opf, 'r', encoding='utf-8') as f:
            content = f.read().format(publisher=self.__publisher, source=self.__source, rights=self.__rights,
                                      date=today, subject=subject, items=items, itemsref=itemrefs,
                                      title=self.__title, author=self.__author, description=self.__intro)
            self.__epub.writestr('OPS/fb.opf', content)
        return self

    def write_cover_page(self):
        """小说封面页"""
        with open(self.__cover_page, 'r', encoding='utf-8') as f:
            content = f.read().format(publisher=self.__publisher, builder=self.__builder, rights=self.__rights,
                                      title=self.__title, author=self.__author, intro=self.__intro)
            self.__epub.writestr('OPS/coverpage.html', content)
        return self

    def get_image(self):
        try:
            response = requests.get(self.__cover)
            if response.status_code == 200:
                return response.content
            return None
        except ConnectionError as e:
            print('请求错误', e.args)
        except Timeout as e:
            print('请求超时', e.args)

    def write_cover(self):
        image = self.get_image()
        self.__epub.writestr('OPS/images/cover.jpg', image)
        return self

    def write_ncx(self):
        # 生成 navPoint
        nav_points = []
        for i, chapter in enumerate(self.__chapters):
            nav_points.append('''
<navPoint id="chapter{id}" playOrder="{id}">
<navLabel><text>{title}</text></navLabel>
<content src="chapter{id}.html"/>
</navPoint>'''.format(id=(i+1), title=chapter['title']))
        nav_points = '\n'.join(nav_points)
        uuid = uuid4()
        with open(self.__ncx, 'r', encoding='utf-8') as f:
            content = f.read().format(uuid4=uuid, provider=self.__provider, builder=self.__builder,rights=self.__rights,
                                      title=self.__title, author=self.__author, nav_points=nav_points)
            self.__epub.writestr('OPS/fb.ncx', content)
        return self

    def write_chapters(self):
        """生成章节内容"""
        with open(self.__chapter, 'r', encoding='utf-8') as f:
            content = f.read()
        for i, chapter in enumerate(self.__chapters):
            html = content.format(provider=self.__provider, builder=self.__builder, rights=self.__rights,
                                  title=chapter['title'], content=chapter['content'])
            self.__epub.writestr('OPS/chapter{}.html'.format(i+1), html)
        return self

    def make(self):
        self.write_mimetype()
        self.write_container()
        self.write_opf()
        self.write_ncx()
        self.write_cover_page()
        self.write_cover()
        self.write_chapters()
        print('epub 已生成')
