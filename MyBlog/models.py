# -*- coding: utf-8 -*-

from exts import db
from datetime import datetime
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class BlogContent(db.Model):
    __tablename__ = 'blog_content'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # now()获取服务器第一次运行的时间
    # now是每次创建一个模型的时候都获取当前时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref=db.backref('BlogContent'))

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog_content.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    blog = db.relationship('BlogContent', backref=db.backref('Comments', order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('Comments'))
