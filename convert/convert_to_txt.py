# !/usr/bin/python
# -*- coding: UTF-8 -*-
from convert.converter import Converter
from config.settings import TXT_DIR
import os


class ConvertToTxt(Converter):
    """
    生成 TXT 格式小说
    """

    def __init__(self, filename):
        # 如果目录不存在，则创建一个
        if not os.path.isdir(TXT_DIR):
            os.mkdir(TXT_DIR)
        self.__dir = TXT_DIR
        self.__filename = self.__dir + filename + '.txt'
        self.__file = open(self.__filename, encoding='utf-8', mode='a')

    def __del__(self):
        """释放文件资源"""
        self.__file.close()

    def __make_info(self, title, author, intro):
        """写入小说基本信息"""
        self.__file.write('《' + title + '》' + '\n')
        self.__file.write('作者：' + author + '\n' * 2)
        self.__file.write('内容简介：' + '\n')
        self.__file.write(intro + '\n' *2)

    def __make_chapter(self, chapter, content):
        """
        将单章内容写入 TXT
        :param chapter: 章节名
        :param content: 章节内容
        :return:
        """
        self.__file.write(chapter + '\n' * 2)
        self.__file.write(content + '\n' * 3)

    def make(self, title, author, intro, chapters):
        self.__make_info(title, author, intro)
        for chapter in chapters:
            self.__make_chapter(chapter['title'], chapter['content'])
