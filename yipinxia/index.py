# !/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import time


base_url = "http://www.yipinxia.net"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.100 Safari/537.36'
}


def get_chapters_page(url):
    """
    获取小说章节目录页源码
    :param url: 页面url
    :return: html代码
    """
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content.decode('gbk')
    return None


def parse_chapters_page(html):
    """
    解析小说章节目录源码
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, 'html.parser')
    lst = soup.find('div', class_="list")
    title = soup.h1.string
    chapters = []
    for li in lst.select('li'):
        if li.a is not None:
            chapters.append((li.a['href'], li.a.string))
    return title, chapters


def get_one_chapter_page(url):
    """
    获取单章页源码
    :param url:
    :return:
    """
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    return None


def parse_one_chapter(html):
    """
    解析单章源码
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find("div", id="booktext")
    # <div id="wcr"><script src="/css/js/bd300.txt" type="text/javascript"></script></div>
    return text.get_text()


def write_to_file(filename, title, content):
    """
    把章节目录和内容写入文件
    :param filename:
    :param title:
    :param content:
    :return:
    """
    file = open(filename, 'a', encoding="utf-8")
    file.write(title + '\n')
    file.write(content + '\n')
    file.close()


def main(start, end):
    for bookId in range(start, end+1):
        url = base_url + "/shu/" + str(bookId) + '/'
        html = get_chapters_page(url)
        title, chapters = parse_chapters_page(html)
        print("正在下载", title)
        filename = title + '.txt'
        for chapter in chapters:
            chapter_url = base_url + chapter[0]
            print("正在下载章节", chapter[1])
            print("章节链接", chapter_url)
            chapter_html = get_one_chapter_page(chapter_url)
            text = parse_one_chapter(chapter_html)
            write_to_file(filename, chapter[1], text)
            print(chapter[1], "done!")
            time.sleep(1.5)  # 隔几秒爬一次
        print(title, "下载完成")


if __name__ == '__main__':
    main(3630, 3630)
