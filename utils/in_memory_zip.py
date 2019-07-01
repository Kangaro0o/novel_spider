# !/usr/bin/python
# -*- coding: UTF-8 -*-
import zipfile
from io import StringIO
from os import path


class InMemoryZip:
    """把写入内存中的文件压缩生成zip"""

    def __init__(self):
        # 创建内存文件
        self.__memory_zip = StringIO()

    def append(self, filename_in_zip, file_content):
        """
        写文本内容到zip
        :param filename_in_zip: 在 zip 中文件的名字
        :param file_content: 文件内容
        :return:
        """
        zf = zipfile.ZipFile(self.__memory_zip, 'a', zipfile.ZIP_DEFLATED, False)
        zf.writestr(filename_in_zip, file_content)
        for zfile in zf.filelist:
            zfile.create_system = 0
        return self

    def append_file(self, file_path, filename_in_zip=None):
        """
        添加本地文件到内存zip文件
        :param file_path: 本地文件全路径
        :param filename_in_zip: 在 zip 中文件的名字
        :return:
        """
        if filename_in_zip is None:
            filename_in_zip = path.split(file_path)[1]
        zf = zipfile.ZipFile(self.__memory_zip, 'a', zipfile.ZIP_DEFLATED, False)
        zf.write(file_path, filename_in_zip)
        for zfile in zf.filelist:
            zfile.create_system = 0
        return self

    def read(self):
        """读取zip文件内容"""
        self.__memory_zip.seek(0)
        return self.__memory_zip.read()

    def write_to_file(self, filename):
        """写zip文件到磁盘"""
        file = open(filename, 'wb')
        file.write(self.read())
        file.close()
