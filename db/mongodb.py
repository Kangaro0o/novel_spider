# !/usr/bin/python
# -*- coding: UTF-8 -*-

from db.database import Database
from pymongo import MongoClient
from config.dbs import MONGO_HOST, MONGO_PORT, MONGO_DB


class MongoDB(Database):
    """
    MongoDB 操作类
    """
    def __init__(self, collection_name):
        """
        初始化 MongoDB 连接参数
        :param collection_name: 保存到哪个集合
        """
        super(MongoDB, self).__init__()
        self.__host = MONGO_HOST
        self.__port = MONGO_PORT
        self.__client = MongoClient(host=self.__host, port=self.__port)
        self.__db = self.__client[MONGO_DB]
        self.__collection = self.__db[collection_name]

    def __del__(self):
        """析构函数 释放资源"""
        self.__client.close()

    def add(self, data):
        print(data)
        return self.__collection.insert_one(data).inserted_id

    def find(self, _id):
        return self.__collection.find({'_id': _id})

    def update(self, _id, data):
        self.__collection.update_one({'_id': _id}, {'$set': data})

    def append(self, _id, data):
        self.__collection.update({'_id': _id}, {'$push': data})
