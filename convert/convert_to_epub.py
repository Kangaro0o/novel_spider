# !/usr/bin/python
# -*- coding: UTF-8 -*-
from convert.converter import Converter
from config.settings import EPUB_DIR, EPUB_SOURCE, EPUB_RIGHTS, EPUB_PUBLISHER, EPUB_BUILDER, EPUB_PROVIDER
import os
from datetime import date
from uuid import uuid4
from utils.in_memory_zip import InMemoryZip
import requests
from requests.exceptions import ConnectionError, Timeout


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
        self.__opf = open(self.templates_path + 'OPS/fb.opf',
                          encoding='utf-8', mode='r')
        self.__coverpage = open(self.templates_path + 'OPS/coverpage.html',
                                encoding='utf-8', mode='r')
        self.__ncx = open(self.templates_path + 'OPS/fb.ncx',
                          encoding='utf-8', mode='r')
        self.__chapter = open(self.templates_path + 'OPS/chapter_template.html',
                              encoding='utf-8', mode='r')
        # 内存中的 zip
        self.__imz = InMemoryZip()

    def __del__(self):
        self.__mimetype.close()
        self.__container.close()
        self.__opf.close()
        self.__coverpage.close()
        self.__ncx.close()
        self.__chapter.close()

    def __set_mimetype(self):
        return self.__mimetype.read()

    def set_container(self):
        return self.__container.read()

    def set_cover(self):
        """小说封面"""
        content = self.__coverpage.read()
        return content.format(publisher=self.__publisher, builder=self.__builder,
                              rights=self.__rights, title=self.__title, author=self.__author, intro=self.__intro)

    def set_ncx(self):
        # 生成 navPoint
        nav_points = []
        for i, chapter in enumerate(self.__chapters):
            nav_points.append('''
<navPoint id="chapter{id}" playOrder="{id}">
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
        生成 fb.opf
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

    def make(self):
        # 因为 mimetype 不需要修改，所以可以直接放到 zip
        self.__imz.append_file(self.templates_path + 'mimetype')
        # 同理，可以直接把 container.xml 放到zip
        self.__imz.append_file(
            self.templates_path + 'META-INF/container.xml', '/META-INF/container.xml')
        # 同理，添加 css/main.css
        self.__imz.append_file(self.templates_path + 'OPS/css/main.css', '/OPS/css/main.css')
        # 获取package.opf
        opf = self.set_opf()
        # 把 fb.opf 放到 zip
        self.__imz.append('/OPS/fb.opf', opf)
        # 获取 fb.ncx
        ncx = self.set_ncx()
        # 把 fb.ncx 放到 zip
        self.__imz.append('/OPS/fb.ncx', ncx)
        # 获取封面
        img = self.get_image()
        # 把封面放到 zip (/OPS/images/cover.jpg)
        self.__imz.append('/OPS/images/cover.jpg', img)
        # 把 coverpage.html 放到 zip
        coverpage = self.set_cover()
        self.__imz.append('/OPS/coverpage.html', coverpage)
        # 获取章节内容
        for i, chapter in enumerate(self.__chapters):
            title = chapter['title']
            content = chapter['content']
            self.__imz.append(
                '/OPS/chapter{id}.html'.format(id=(i+1)), self.set_chapter(title, content))
        self.__imz.write_to_file(self.__title + '.epub')
