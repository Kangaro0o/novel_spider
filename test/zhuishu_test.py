# !/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
from novel.zhuishu_spider import ZhuiShuSpider
from config.urls import ZhuiShu_Index

class ZhuiShuTest(unittest.TestCase):
    """
    追书网爬虫测试类
    """
    def setUp(self):
        """初始化"""
        print("-----------init-------------")
        self.site_url = ZhuiShu_Index
        self.zhuishu_spider = ZhuiShuSpider()

    def tearDown(self):
        """清理测试环境"""
        print("-----------clear--------------")

    def test_search(self):
        search_url = self.zhuishu_spider.search('元尊')
        self.assertEqual('https://www.bimo.cc/search.aspx?keyword=%E5%85%83%E5%B0%8A', search_url)


if __name__ == '__main__':
    unittest.main()