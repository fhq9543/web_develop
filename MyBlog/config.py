# -*- coding: utf-8 -*-
import os

if os.path.exists('config_local.py'):
    from config_local import *

# 数据库配置
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': 'a',
    'charset': 'utf8',
    'db': 'myblog',
    }

# 服务器配置
WEB_CONFIG = {
    'debug': True,
    'host': '0.0.0.0',
    'port': 8801,
}

# db
SECRET_KEY = '9B\xb7\xfe\xe2\xfd=\x17\xefY\xbf\xfb\x0e\x18Q\xc2\xbfr\x92\xc9\xbb\xb8\xac\xd0'
SQLALCHEMY_DATABASE_URI = "mysql://{user}:{passwd}@{host}:{port}/{db}?charset={charset}".format(**DB_CONFIG)
SQLALCHEMY_TRACK_MODIFICATIONS = False
