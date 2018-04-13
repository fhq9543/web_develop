# coding=utf-8
import os
import uuid
import magic
from datetime import datetime, date

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

import cropresize2
import short_url
from PIL import Image
from flask import abort, request
from werkzeug.utils import cached_property

from .mimes import IMAGE_MIMES, AUDIO_MIMES, VIDEO_MIMES
from .utils import get_file_md5, get_file_path
from . import db

class CRUD():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

class PasteFile(db.Model, CRUD):
    __tablename__ = 'PasteFile'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(5000), nullable=False)
    filehash = db.Column(db.String(128), nullable=False, unique=True)
    filemd5 = db.Column(db.String(128), nullable=False, unique=True)
    uploadtime = db.Column(db.DateTime, nullable=False)
    mimetype = db.Column(db.String(256), nullable=False)
    size = db.Column(db.Integer, nullable=False)

    def __init__(self, filename='', mimetype='application/octet-stream',
                 size=0, filehash=None, filemd5=None):
        self.uploadtime = datetime.now()
        self.mimetype = mimetype
        self.size = int(size)
        self.filehash = filehash if filehash else self._hash_filename(filename)
        self.filename = filename if filename else self.filehash
        self.filemd5 = filemd5

    def to_dict(self, fields=None, date_to_str=True):
        '''
        将model转化为dict
            param fields：要取出的字段
            param date_to_str：是否将日期转化为字符串。格式为 2018-01-01 11:11:11
            return：dict or None
        '''
        if not hasattr(self, '__table__'):
            return

        def convert_data(value):
            if date_to_str:
                return value if not isinstance(value, (datetime, date)) else str(value)
            else:
                return value

        if not fields:
            return {col: convert_data(getattr(self, col, None))
                    for col in self.__table__.columns.keys()}
        else:
            return {key: convert_data(getattr(self, key, None))
                    for key in fields}

    @staticmethod
    def _hash_filename(filename):
        _, _, suffix = filename.rpartition('.')
        return '%s.%s' % (uuid.uuid4().hex, suffix)

    @cached_property
    def symlink(self):
        '''
        通过ID生成短链接地址
        '''
        return short_url.encode_url(self.id)

    @classmethod
    def get_by_symlink(cls, symlink, code=404):
        '''
        通过短链接找对应数据库条目
        '''
        id = short_url.decode_url(symlink)
        return cls.query.filter_by(id=id).first() or abort(code)

    @classmethod
    def get_by_filehash(cls, filehash, code=404):
        '''
        从数据库找匹配hash值
        '''
        return cls.query.filter_by(filehash=filehash).first() or abort(code)

    @classmethod
    def get_by_md5(cls, filemd5):
        '''
        从数据库匹配md5值
        '''
        return cls.query.filter_by(filemd5=filemd5).first()

    @classmethod
    def create_by_upload_file(cls, uploaded_file):
        '''
        上传文
        判断hash值，如果上传过返回之前上传的文件
        '''
        rst = cls(uploaded_file.filename, uploaded_file.mimetype, 0)
        uploaded_file.save(rst.path)
        with open(rst.path, 'rb') as f:
            filemd5 = get_file_md5(f)
            uploaded_file = cls.get_by_md5(filemd5)
            if uploaded_file:
                os.remove(rst.path)
                return uploaded_file
        filestat = os.stat(rst.path)
        rst.size = filestat.st_size
        rst.filemd5 = filemd5
        return rst

    @classmethod
    def create_by_old_paste(cls, filehash):
        filepath = get_file_path(filehash)
        mimetype = magic.from_file(filepath, mime=True)
        filestat = os.stat(filepath)
        size = filestat.st_size

        rst = cls(filehash, mimetype, size, filehash=filehash)
        return rst

    @property
    def path(self):
        return get_file_path(self.filehash)

    def get_url(self, subtype, is_symlink=False):
        hash_or_link = self.symlink if is_symlink else self.filehash
        return 'http://{host}/{subtype}/{hash_or_link}'.format(
            subtype=subtype, host=request.host, hash_or_link=hash_or_link)

    @property
    def url_i(self):
        '''
        获取源文件地址
        '''
        return self.get_url('i')

    @property
    def url_p(self):
        '''
        获取文件预览地址
        '''
        return self.get_url('preview')

    @property
    def url_s(self):
        '''
        获取文件短链接地址
        '''
        return self.get_url('s', is_symlink=True)

    @property
    def url_d(self):
        '''
        获取文件下载地址
        '''
        return self.get_url('download')

    @property
    def image_size(self):
        if self.is_image:
            f = open(self.path, 'rb')
            im = Image.open(f)
            return im.size
        return (0, 0)

    @property
    def quoteurl(self):
        '''
        屏蔽url中特殊的字符
        '''
        return quote(self.url_i)

    @property
    def is_image(self):
        return self.mimetype in IMAGE_MIMES

    @property
    def is_audio(self):
        return self.mimetype in AUDIO_MIMES

    @property
    def is_video(self):
        return self.mimetype in VIDEO_MIMES

    @property
    def is_pdf(self):
        return self.mimetype == 'application/pdf'

    @property
    def type(self):
        for t in ('image', 'pdf', 'video', 'audio'):
            if getattr(self, 'is_' + t):
                return t
        return 'binary'
