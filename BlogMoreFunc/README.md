# Blog
一个简单的博客

## 环境

    python3.6
    sqlite3

## 使用方法

    下载：
        git clone git@github.com:fhq9543/web_develop.git

    配置：
        pip install -r requirements.txt
        修改config配置

    运行：
        python manage.py db init
        python manage.py db migrate
        python manage.py db upgrade
        python manage.py runserver

    生成虚拟用户和文章：
        访问：127.0.0.1:5000/generate
        生成的虚拟用户其密码都为 1

