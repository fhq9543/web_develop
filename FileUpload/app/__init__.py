# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug import SharedDataMiddleware
from .utils import get_file_path, humanize_bytes

db = SQLAlchemy()

# 工厂函数
def create_app(config_name):
    app = Flask(__name__, template_folder='./templates',
                static_folder='./static')
    app.config.from_object(config_name)

    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/i/': get_file_path()
    })

    db.init_app(app)

    #注册蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
