#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2017/6/10.
@author: yangbaohu
'''

import re
import json
from urllib import quote, unquote
from urlparse import urlparse
from datetime import datetime

from flask import Flask, redirect, jsonify, request, abort, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_restful import Api, Resource

from utils import DEFAULT_ENCODER

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
api = Api(app)
cache = FlaskRedis(app)

LOCALHOST = app.config['LOCALHOST']
EXPIRE_TIME = app.config['EXPIRE_TIME']


def update_cache(short_url, long_url, expire_time=EXPIRE_TIME):
    cache.set(''.join(['short2long', ':', short_url]), long_url, ex=expire_time)
    cache.set(''.join(['long2short', ':', long_url]), short_url, ex=expire_time)


class Url(db.Model):
    __tablename__ = 'long2short'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    long_url = db.Column(db.String(512))
    short_url = db.Column(db.String(50))
    url_type = db.Column(db.CHAR(1))
    create_time = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Url %r>' % self.id


def get_real_url(url):
    """给 URL 添加 scheme(qq.com -> http://qq.com)"""
    # 支持的 URL scheme
    # 常规 URL scheme
    scheme2 = re.compile(r'(?i)^[a-z][a-z0-9+.\-]*://')
    # 特殊 URL scheme
    scheme3 = ('git@', 'mailto:', 'javascript:', 'about:', 'opera:',
               'afp:', 'aim:', 'apt:', 'attachment:', 'bitcoin:',
               'callto:', 'cid:', 'data:', 'dav:', 'dns:', 'fax:', 'feed:',
               'gg:', 'go:', 'gtalk:', 'h323:', 'iax:', 'im:', 'itms:',
               'jar:', 'magnet:', 'maps:', 'message:', 'mid:', 'msnim:',
               'mvn:', 'news:', 'palm:', 'paparazzi:', 'platform:',
               'pres:', 'proxy:', 'psyc:', 'query:', 'session:', 'sip:',
               'sips:', 'skype:', 'sms:', 'spotify:', 'steam:', 'tel:',
               'things:', 'urn:', 'uuid:', 'view-source:', 'ws:', 'xfire:',
               'xmpp:', 'ymsgr:', 'doi:',
               )
    url_lower = url.lower()

    # 如果不包含规定的 URL scheme，则给网址添加 http:// 前缀
    scheme = scheme2.match(url_lower)
    if not scheme:
        for scheme in scheme3:
            url_splits = url_lower.split(scheme)
            if len(url_splits) > 1:
                break
        else:
            url = 'http://' + url
    return url


def save_url(url):
    db.session.add(url)
    db.session.commit()
    short_url = DEFAULT_ENCODER.encode_url(url.id)
    url.short_url = short_url
    db.session.add(url)
    return url


def delete_url(url):
    db.session.delete(url)
    db.session.commit()


def get_long_url(short_url):
    long_url = cache.get(''.join(['short2long', ':', short_url]))  # 缓存中查询
    if not long_url:
        url = Url.query.filter_by(short_url=short_url).first()
        if url:
            long_url = url.long_url
            update_cache(short_url, long_url)
        else:
            long_url = ''
    return long_url


class Index(Resource):
    def get(self):
        return "THIS IS LONG2SHORT URL INDEX!"


class Access(Resource):
    def get(self, short_url):
        long_url = get_long_url(short_url)
        if not long_url:
            abort(404)
        return redirect(unquote(long_url), code=302)


class Short2Long(Resource):
    def get(self):
        data = request.args
        return self._short2long(data)

    def post(self):
        data = json.loads(request.data)
        return self._short2long(data)

    def _short2long(self, data):
        short_url = data.get('short_url')
        if not short_url.startswith(LOCALHOST):
            return jsonify({'long_url': ''})
        short_url = urlparse(short_url).path.split('/')[1]
        long_url = get_long_url(short_url)
        return jsonify({'long_url': unquote(long_url)})


class Long2Short(Resource):
    def post(self):
        data = json.loads(request.data)
        return self._long2short(data)

    def get(self):
        data = request.args
        return self._long2short(data)

    def _long2short(self, data):
        url_type = data.get('url_type', 's')  # 获取短链类型，默认为's'、表示短期存在，默认时间为一周，'l'为永久存在redis中
        long_url = data.get('long_url')
        long_url = get_real_url(long_url)
        long_url = quote(long_url)

        temp = ':'.join(['long2short', long_url])
        if temp in cache.keys('long2short:*'):
            short_url = cache.get(temp)
        else:
            url = Url(long_url=long_url, url_type=url_type)
            url = save_url(url)
            short_url = url.short_url
            if short_url:
                if url_type == 'l':
                    update_cache(short_url, long_url, expire_time=None)
                elif url_type == 's':
                    update_cache(short_url, long_url)
            else:
                delete_url(url)
                short_url = ''
        short_url = ''.join([LOCALHOST, short_url])
        return jsonify({'short_url': short_url})


api.add_resource(Index, '/')
api.add_resource(Access, '/<short_url>')
api.add_resource(Short2Long, '/short2long')
api.add_resource(Long2Short, '/long2short')

if __name__ == '__main__':
    # db.create_all()
    app.debug = True
    app.run()
