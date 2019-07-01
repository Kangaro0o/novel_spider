# !/usr/bin/python
# -*- coding: UTF-8 -*-


class Database:
    """
    数据库操作的父类
    """

    def __init__(self):
        pass

    def add(self, data):
        """创建新数据"""
        pass

    def delete(self):
        """删除数据"""
        pass

    def append(self, _id, data):
        """追加数据（仅在非关系型数据库有用）"""
        pass

    def update(self, _id, data):
        """更新数据"""
        pass

    def find_by_id(self, _id):
        """通过查找数据"""
        pass

    def find(self, **kwargs):
        """多条件搜素"""
        pass
