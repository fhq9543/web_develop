# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session
from models import User, BlogContent, Comment
from exts import db
import config
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    context = {
            'blogs': BlogContent.query.order_by('-create_time').all()
            }
    return render_template('index.html', **context)

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user_query = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user_query:
            session['user_id'] = user_query.id
            # 如果想在31天内都不需要登录
            is_remenber = request.form.get('is_remenber')
            if is_remenber == '1':
                session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或者密码错误，请确认后再登录！'

@app.route('/register/', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # 手机号码验证，看下是否已经注册
        user_query = User.query.filter(User.telephone == telephone).first()
        if user_query:
            return u'该号码已注册！'
        else:
            if password1 != password2:
                return u'两次输入密码不同，请重新输入！'
            else:
                user = User(telephone = telephone, username = username, password = password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/writeblog/', methods=['GET', 'POST'])
@login_required
def writeblog():
    if request.method =='GET':
        return render_template('writeblog.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        blog = BlogContent(title = title, content = content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        blog.author = user
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<blog_id>', methods=['GET', 'POST'])
def detail(blog_id):
    blog = BlogContent.query.filter(BlogContent.id == blog_id).first()
    return render_template('detail.html', blog = blog)

@app.route('/add_comment/', methods=['POST'])
@login_required
def add_comment():
    content = request.form.get('blog_comment')
    blog_id = request.form.get('blog_id')
    comment = Comment(content = content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    comment.author = user
    blog = BlogContent.query.filter(BlogContent.id == blog_id).first()
    comment.blog = blog
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail', blog_id = blog_id))


if __name__ == '__main__':
    app.run(**config.WEB_CONFIG)
