# !/usr/bin/python
# -*- coding: UTF-8 -*-

from novel.zhuishu_spider import ZhuiShuSpider
from db.mongodb import MongoDB
from utils.novel import Novel
import time


zhuishu_spider = ZhuiShuSpider()
mongodb = MongoDB('zhuishu')
# novel = Novel(zhuishu_spider, mongodb)

# kw = '永夜'
# novel.fuzzy_search(kw)

# zhuishu = ZhuiShuSpider()
# search_html = zhuishu.get_search_html("美女")
# results = zhuishu.get_search_results("龙王")
# first = results[0]
# chapters_html = zhuishu.get_chapters_html(first['chapters_url'])
# novel_info = zhuishu.get_novel_info(chapters_html)
# print(novel_info)
# chapters = zhuishu.get_chapters(chapters_html)
# for chapter in chapters:
#     print(chapter)

novel = Novel(zhuishu_spider, mongodb)
novel.fuzzy_search('赞歌')