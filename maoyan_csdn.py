# coding: utf-8
"""
@author: Evan
@time: 2019/12/24 14:56
"""
import json
import requests
from requests.exceptions import RequestException
import re
import time


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML,'
                          + ' like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<h4.*?href="(.*?)".*?article-type.*?>(.*?)</span>?(\s+)(.+?)(\s+?)</a>'
                         + '.*?class="date">?(\s+)(.*?)<.*?class="num">(\d+?)</span>'
                         + '.*?class="num">(\d+?)</span>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'url': item[0],
            'type': item[1],
            'title': item[3],
            'date': item[6],
            'read_num': item[7],
            'comm_num': item[8]
        }


def write_to_file(content):
    with open('result_blog.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'https://blog.csdn.net/Yuyh131/article/list/' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(1, 11):
        main(offset=i)
        time.sleep(4)
