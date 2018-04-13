# File Upload
文件上传下载系统

## 环境

    python3.6
    mysql5.7

## 使用方法

    git clone git@github.com:fhq9543/web_develop.git
    (注意我使用的版本是python3.6)
    pip install -r requirements.txt
    修改config配置
    创建数据库FileLib
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py runserver
