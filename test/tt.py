#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2017/6/21.
@author: yangbaohu
'''

import requests
import json


def long2short_post(long_url, url_type='s'):
    url = 'http://127.0.0.1:5000/long2short'
    data = {
        'long_url': long_url,
        'url_type': url_type
    }
    return requests.post(url, json=data).json()


def long2short_get(long_url, url_type='s'):
    url = 'http://127.0.0.1:5000/long2short?long_url=%s&url_type=%s' % (long_url, url_type)
    content = requests.get(url).content
    return json.loads(content)


def short2long_post(short_url):
    url = 'http://127.0.0.1:5000/short2long'
    data = {
        'short_url': short_url
    }
    return requests.post(url, json=data).json()


def short2long_get(short_url):
    url = 'http://127.0.0.1:5000/short2long?short_url=%s' % short_url
    return requests.get(url).content


if __name__ == '__main__':
    urls = [
        'http://database.51cto.com/art/201006/205223.htm',
        'http://nbviewer.jupyter.org/github/donnemartin/data-science-ipython-notebooks/tree/master/',
        'https://pypi.python.org/pypi',
        'http://tool.oschina.net/codeformat/xml/',
        'https://github.com/jobbole/awesome-python-cn',
        'http://scikit-learn.org/stable/tutorial/index.html',
        'https://grouplens.org/datasets/movielens/',
        'http://blog.jobbole.com/110558/',
        'http://helper.gemii.cc:8082/static/index.html',
        'https://github.com/nryoung/algorithms',
        'http://code.ziqiangxuetang.com/django/django-orm-standalone.html',
        'https://my.oschina.net/jarly/blog/898144',
        'http://www.360.cn',
        'http://www.baidu.com',
    ]
    for i in range(1):
        for j, url in enumerate(urls):
            _type = 's' if j % 2 else 'l'
            print(_type)
            print(long2short_post(url, _type))
    print('end!')
