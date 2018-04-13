# -*- coding: utf-8 -*-
UPLOAD_FOLDER = '/tmp/permdir'
# MYSQL
mysql_db_username = 'root'
mysql_db_password = '1234'
mysql_db_name = 'FileLib'
mysql_db_hostname = 'localhost'

SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "SOME SECRET"

# MySQL
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=mysql_db_username,
                                                                                        DB_PASS=mysql_db_password,
                                                                                        DB_ADDR=mysql_db_hostname,
                                                                                        DB_NAME=mysql_db_name)
