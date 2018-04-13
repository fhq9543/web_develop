# -*- coding: utf-8 -*-
from .. import db
from ..models import PasteFile
from ..mimes import IMAGE_MIMES
from . import main
from ..utils import get_file_path, humanize_bytes

import os
from flask import abort, Flask, request, jsonify, redirect, send_file, render_template, url_for, make_response, Response

from collections import Iterable

ONE_MONTH = 60 * 60 * 24 * 30

@main.route('/download/<filehash>', methods=['GET'])
def download(filehash):
    '''
    文件下载
    '''
    paste_file = PasteFile.get_by_filehash(filehash)

    return send_file(open(paste_file.path, 'rb'),
                     mimetype='mainlication/octet-stream',
                     cache_timeout=ONE_MONTH,
                     as_attachment=True,
                     attachment_filename=paste_file.filename.encode('utf-8'))


@main.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@main.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html', **locals())
    else:
        uploaded_file = request.files['file']
        print("**************************")
        print(uploaded_file)
        if not uploaded_file:
            return abort(400)

        paste_file = PasteFile.create_by_upload_file(uploaded_file)
        paste_file.add(paste_file)
        return redirect(url_for('main.preview', filehash=paste_file.filehash))


@main.route('/fileList', methods=['GET', 'POST'])
def fileList():
    if request.method == 'GET':
        file_all = PasteFile.query.all()
        fields = ['filename', 'filehash', 'uploadtime', 'mimetype', 'size']
        files = [f.to_dict(fields=fields) for f in file_all]
        return render_template('fileList.html', files = files)
    elif request.method == 'POST':
        filename = request.form.get('name')
        if filename:
            search = PasteFile.query.filter(PasteFile.filename.like('%s%%' % filename)).all()
            print('%%%%%%%%%%')
            print(search[0].filename)
        else:
            search = PasteFile.query.all()
        fields = ['filename', 'filehash', 'uploadtime', 'mimetype', 'size']
        res = [f.to_dict(fields=fields) for f in search]
        return render_template('fileList.html', files = res)


@main.route('/delete/<filename>', methods=['GET'])
def delete(filename):
    search = PasteFile.query.filter_by(filename=filename).first()
    try:
        search.delete(search)
        res = jsonify({"status":"1"})
        return res
    except Exception as e:
        db.session.rollback()
        res = jsonify({"status":"0"})
        return res


@main.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@main.route('/preview/<filehash>')
def preview(filehash):
    '''
    文件预览
    '''
    paste_file = PasteFile.get_by_filehash(filehash)

    if not paste_file:
        filepath = get_file_path(filehash)
        if not(os.path.exists(filepath) and (not os.path.islink(filepath))):
            return abort(404)

        paste_file = PasteFile.create_by_old_paste(filehash)
        paste_file.add(paste_file)

    return render_template('preview.html', p=paste_file)


@main.route('/id/<symlink>')
def s(symlink):
    '''
    文件hash值太长，通过短链接访问
    '''
    paste_file = PasteFile.get_by_symlink(symlink)

    return redirect(paste_file.url_p)

