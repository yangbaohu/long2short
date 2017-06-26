#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2017/5/16.
@author: yangbaohu
'''
# 系统配置
SECRET_KEY = 'Ud82GgcSXaHq1bkt4foYzOJDCwu5ZBh3yl0FEV9TnpK7QxmIrMWAe6ivNRPLsj'

# 数据库配置
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/long2short?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# REDIS
REDIS_URL = 'redis://localhost:6379/0'

# 自有配置
LOCALHOST = 'http://127.0.0.1:5000/'  # 返回短链接前缀
EXPIRE_TIME = 60 * 60 * 24 * 7
